import asyncio
import random
import json


async def get_battery_level():
    battery_level = random.randint(0, 100) # Simulate battery level
    return battery_level

async def battery_level_task(websocket):
    """
    Send the battery level to the client every 30 seconds.
    
    Args:
        websocket: The websocket connection object.
    """
    
    while True:
        try:
            level = await get_battery_level()
            message = json.dumps({"type": "battery", "data": level})
            await websocket.send(message)
            await asyncio.sleep(30)  # Repeat every 30 seconds
        except Exception as e:
            print(f"Error while getting battery level: {e}")
