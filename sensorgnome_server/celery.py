import os
import kombu
from celery import Celery, bootsteps

# Needed to load settings when we're not loading all of Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorgnome_server.settings')

app = Celery('sensorgnome_server')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Task modules loaded from registered app configs.
app.autodiscover_tasks()

with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='sensorgnome-exchange',
        type='fanout',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue = kombu.Queue(
        name='sensorgnome-queue',
        exchange=exchange,
        routing_key='sensorgnome',
        channel=conn,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()


class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()

app.steps['consumer'].add(MyConsumerStep)