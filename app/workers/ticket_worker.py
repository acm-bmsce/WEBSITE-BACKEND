# workers/test_worker.py

import redis
import json

r = redis.Redis(host="localhost", port=6379)
pubsub = r.pubsub()
pubsub.subscribe("ticket_created")

print("Listening...")

for message in pubsub.listen():
    if message["type"] == "message":
        data = json.loads(message["data"])
        print("Received event:", data)