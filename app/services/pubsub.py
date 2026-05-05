from google.cloud import pubsub_v1
import json
import os

project_id = os.getenv("GCP_PROJECT_ID")
topic_id = "ticket-created"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish(message: dict):
    data = json.dumps(message).encode("utf-8")
    publisher.publish(topic_path, data=data)