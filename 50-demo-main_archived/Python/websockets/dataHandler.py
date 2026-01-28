import asyncio

import websockets

from victronConnector import VictronConnector

async def handle_mqtt_client(websocket, topic, db, dbTopic):
    loop = asyncio.get_running_loop()

    victron = VictronConnector(
        host="192.168.137.52",
        port=1883,
        topics=[topic],
        loop=loop
    )
    victron.start()  # MQTT runs in background thread

    try:
        async for msg in victron.get_message():
            payload = msg["payload"]["value"]

            # Send to WebSocket client
            db.table(dbTopic).insert(value=payload) # todo test + maybe not everytime maybe on a interval
            await websocket.send(str(payload))
            print(f"Sent to WS client: {payload}")

            await asyncio.sleep(0.01)  # small delay for stability

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"Error in MQTT handler: {e}")
