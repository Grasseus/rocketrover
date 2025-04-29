# The code in this file was written by me. I used ChatGPT and the docs as reference tools to better understand certain concepts,
# such as WebSockets and function handling. I also used ChatGPT to review and improve code syntax and structure.
# All implementation and final code decisions were made by me after researching and understanding the concepts.

import asyncio
import inspect
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from pydantic import ValidationError
import json

from .commands import get_command_map
from .tasks import battery_level_task


async def sender(websocket):
    """
    Send all the background information to the client.

    Args:
        websocket: The websocket connection object.
    """

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(battery_level_task(websocket))
    except ConnectionClosed:
        print("Client disconnected")


# ChatGPT mainly used for debugging this
async def input_handler(websocket, rover):
    """
    Handle incoming messages from the websocket and executes the corresponding functions.

    The function:
    - Parses the message as JSON.
    - Validates and executes the handler for the command.
    - Handles errors such as invalid JSON, validation issues, and handler errors.

    Args:
        websocket: The websocket connection object.
        rover (Rover): The rover object to interact with based on commands.
    """

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError as e:
                await send_error(websocket, f"Invalid JSON received: {e}")
                continue  # skip this message and wait for the next one

            command_name = data.get("type")
            command_args = data.get("data", {})
            command = get_command_map(rover).get(command_name)

            if command:
                handler = command["handler"]
                args = command["args"]
                try:
                    valid_args = args(**command_args)
                except ValidationError as e:
                    await send_error(websocket, f"Validation error: {e}")
                    continue
                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(**valid_args.dict())
                    else:
                        handler(**valid_args.dict())
                except Exception as e:
                    await send_error(websocket, f"Handler execution error: {e}")

            else:
                await send_error(websocket, f"Function '{command_name}' is not defined")

    except ConnectionClosed:
        print("Client disconnected.")
        await rover.move(0, 0)


async def send_error(websocket, error_msg):
    """
    Send error messages to the client.
    
    Args:
        websocket: The websocket connection object.
        error_msg (str): The error message.
    """
    error_payload = json.dumps({"type": "error", "message": error_msg})
    await websocket.send(error_payload)
    print(error_msg)


# WebSocket handler
async def ws_handler(websocket, rover):
    """
    Handle the websocket tasks.
    
    Args:
        websocket: The websocket connection object.
        rover (Rover): The rover object.
    """
    # Gather consumer and producer tasks
    async with asyncio.TaskGroup() as tg:
        tg.create_task(input_handler(websocket, rover))
        tg.create_task(sender(websocket))


async def start_server(rover):
    """
    Start the websocket server.

    Args:
        rover (Rover): The rover object.
    """
    async with serve(
        lambda websocket: ws_handler(websocket, rover), "", 8080
    ) as server:
        await server.serve_forever()
