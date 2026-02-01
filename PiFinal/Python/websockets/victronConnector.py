import asyncio

import paho.mqtt.client as mqtt
import json

class VictronConnector:
    def __init__(self, host, port=1883, topics=None, loop=None):
        self.host = host
        self.port = port
        self.topics = topics or ["N/+/system/+/Dc/Battery/+"]
        self.client = mqtt.Client()
        self.queue = asyncio.Queue()
        self.loop = loop or asyncio.get_event_loop()
        self.client.on_message = self._on_message

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            payload_json = json.loads(payload)  # parse JSON if applicable
        except Exception:
            payload_json = {"value": payload}  # fallback to raw string

        asyncio.run_coroutine_threadsafe(
            self.queue.put({"topic": msg.topic, "payload": payload_json}),
            self.loop
        )

    def start(self):
        print("Connecting to MQTT broker:", self.host, self.port)

        self.client.connect(self.host, self.port)
        print("Subscribing to topics:", self.topics)

        for topic in self.topics:
            self.client.subscribe(topic)
        # Start MQTT loop in background thread
        self.client.loop_start()
        print("connected")

    async def get_message(self):
        while True:
            msg = await self.queue.get()
            yield msg
