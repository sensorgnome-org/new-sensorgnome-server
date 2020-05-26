import os
from celery import shared_task
from sensorgnome_server.celery import app
from .models import Message
import kombu

os.environ.setdefault("EVENT_CONSUMER_APP_CONFIG", "sensorgnome_server.settings")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorgnome_server.settings')
except RuntimeError:
    pass

from event_consumer import message_handler

@message_handler(routing_keys='sensorgnome-management')
def process_message(body):
    print("Message handler:", body)
    m = Message(payload=body)
    m.save()