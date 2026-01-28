import asyncio

import websockets

from victronConnector import VictronConnector

async def handle_mqtt_client(websocket, topic, db):
    loop = asyncio.get_running_loop()

    victron = VictronConnector(
        host="169.254.1.2",  # Fixed IP typo: should be 169 not 168
        port=1883,
        topics=[topic],
        loop=loop
    )
    victron.start()  # MQTT runs in background thread

    try:
        async for msg in victron.get_message():
            payload = msg["payload"]

            # Send to WebSocket client
            db.table(topic).insert(value=payload["value"]) # todo test + maybe not everytime maybe on a interval
            await websocket.send(payload["value"])
            print(f"Sent to WS client: {payload["value"]}")

            await asyncio.sleep(0.01)  # small delay for stability

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"Error in MQTT handler: {e}")
