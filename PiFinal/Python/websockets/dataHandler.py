import asyncio

import websockets

from victronConnector import VictronConnector

async def handle_mqtt_client(websocket, topic, db, dbTopic):
    loop = asyncio.get_running_loop()

    victron = VictronConnector(
        host="192.168.1.101",
        port=1883,
        topics=[topic],
        loop=loop
    )
    victron.start()  # MQTT runs in background thread

    try:
        async for msg in victron.get_message():
            payload = msg["payload"]["value"]

            payload_str = f"{float(payload):.2f}"

            db.table(dbTopic).insert(value=payload_str)
            await websocket.send(payload_str)

            print(f"Sent to WS client: {payload_str}")

            await asyncio.sleep(0.01)  # small delay for stability

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"Error in MQTT handler: {e}")
