import asyncio
import random

import websockets

from dataHandler import handle_mqtt_client
from databaseManager.DatabaseManager import DatabaseManager
db = DatabaseManager(user="root", password="root", host="mysql-windgen")


async def handle_client(websocket):
    path = websocket.request.path

    print(f"Client connected to path: {path}")

    match path:
        case "/volt":
            print("connected to volt")

            await handle_mqtt_client(websocket, "N/+/system/+/Dc/Battery/Voltage", db, "voltage_data"),
        case "/amp":
            print("connected to amp")

            await handle_mqtt_client(websocket, "N/+/system/+/Dc/Battery/Current", db, "amp_data")
        case "/SoC":
            print("connected to soc")

            await return_random(websocket)  # todo make handler
        case _:
            print("incorrect path")
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
