import os
import kombu
from celery import Celery, bootsteps
import django

# Needed before event_consumer is imported.
os.environ.setdefault("EVENT_CONSUMER_APP_CONFIG", "sensorgnome_server.settings")

# Needed to load settings when we're not loading all of Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorgnome_server.settings')

django.setup()

from event_consumer.handlers import AMQPRetryConsumerStep

app = Celery('sensorgnome_server')
app.steps['consumer'].add(AMQPRetryConsumerStep)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
