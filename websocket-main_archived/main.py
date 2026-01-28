import asyncio
import random

import websockets

from dataHandler import handle_mqtt_client
from databaseManager.databaseManager import DatabaseManager as databaseManager
db = databaseManager(user="admin", password="root", host="192.168.2.121:3306")


async def handle_client(websocket):
    path = websocket.request.path

    print(f"Client connected to path: {path}")

    match path:
        case "/volt":
            await handle_mqtt_client(websocket, "N/+/system/+/Dc/Battery/Power", db),
        case "/amp":
            await handle_mqtt_client(websocket, "N/+/system/+/Dc/Battery/Current", db)
        case "/SoC":
            await return_random(websocket)  # todo make handler
        case _:
            await websocket.send("no path supplied")


async def start_websocket_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 32848)
    print("✅ WebSocket server running")
    await server.wait_closed()

async def return_random(websocket):
    try:
        while True:
            await asyncio.sleep(1)
            await websocket.send(str(random.randint(0,300)))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    db.startDB()
    db.createTables()
    asyncio.run(start_websocket_server())
