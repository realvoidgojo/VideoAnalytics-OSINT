# WebSocket server example (alert_server.py)
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(f"Received alert: {message}")
        # You can add logic here to forward the alert to a dashboard
        await websocket.send(f"Alert received: {message}") #Acknowledge receiving the alert

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
