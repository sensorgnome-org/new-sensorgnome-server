import os
from celery import shared_task
from sensorgnome_server.celery import app
from .models import Message
from sg_management.models import SensorGnome
import kombu
import json
import datetime
from django.db import transaction


os.environ.setdefault("EVENT_CONSUMER_APP_CONFIG", "sensorgnome_server.settings")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorgnome_server.settings')
except RuntimeError:
    pass

from event_consumer import message_handler

@message_handler(routing_keys='sensorgnome-management')
def process_message(body):
    try:
        j = json.loads(body)
        print(f"Message from {j['id']}: \"{j['message']}\".")
        for k in j.keys():
            if k not in ("id", "message"):
                print(f"Extra: {k}: {j[k]}.")
        sg = SensorGnome.objects.get(serial=j["id"])
        m = Message(payload=j["message"], sensorgnome=sg)
        with transaction.atomic():
            m.save()
            sg.update_last_seen()
        return True
    except Exception as e:
        print("Exception:", e)
        return True