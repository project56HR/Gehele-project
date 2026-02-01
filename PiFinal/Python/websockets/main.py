import asyncio
import random
import os
import websockets

from dataHandler import handle_mqtt_client
from databaseManager.DatabaseManager import DatabaseManager
db = DatabaseManager(
    user="appuser",
    password="apppass",
    host="mysql",
    database="wind_generator_stats"
)


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
        case "/watt":
            print("connected to watt")

            await handle_mqtt_client(websocket, "N/+/system/+/Dc/Battery/Power", db, "watt_data")

        case "/uptime":
            await uptime(websocket)
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

CLOCK_TICKS = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

def container_uptime():
    with open("/proc/1/stat") as f:
        start_ticks = int(f.read().split()[21])

    with open("/proc/uptime") as f:
        host_uptime = float(f.read().split()[0])

    return host_uptime - (start_ticks / CLOCK_TICKS)

async def uptime(websocket):
    try:
        while True:
            await websocket.send(str(int(container_uptime())))
            await asyncio.sleep(1)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    db.startDB()
    db.createTables()
    asyncio.run(start_websocket_server())
