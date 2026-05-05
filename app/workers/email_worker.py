from google.cloud import pubsub_v1
import json
import asyncio
import os
from app.services.email import send_email

project_id = os.getenv("GCP_PROJECT_ID")
subscription_id = "ticket-created-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    data = json.loads(message.data.decode("utf-8"))

    email = data["email"]
    event_name = data["event_name"]

    print(f"Received → {email}, {event_name}")

    try:
        asyncio.run(send_email(email, event_name))
        print("Email sent ✅")
        message.ack()
    except Exception as e:
        print("Email failed ❌", e)
        # no ack → Pub/Sub will retry
        # (that’s why Pub/Sub is useful)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

print("Worker listening...")

with subscriber:
    streaming_pull_future.result()