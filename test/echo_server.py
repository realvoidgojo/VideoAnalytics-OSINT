import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Server received: {message}")

async def main():
    async with websockets.serve(echo, "localhost", 8765):  # Change port if needed, make sure its the same port as in test_env.py
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
