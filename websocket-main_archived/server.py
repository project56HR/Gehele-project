import asyncio

import websockets

# Replace with your WebSocket URL
WEBSOCKET_URL = "ws://127.0.0.1:32848/volt"

async def connect_to_websocket():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print(f"✅ Connected to {WEBSOCKET_URL}")

            # Listen for messages
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")

    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")

# Run the async function
asyncio.run(connect_to_websocket())
