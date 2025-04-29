import asyncio

from server import start_server
from rover import create_rover

if __name__ == "__main__":
    rover = create_rover()
    asyncio.run(start_server(rover))
