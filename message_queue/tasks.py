from celery import shared_task
from sensorgnome_server.celery import app

def publish_message(message):
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange='sensorgnome-exchange',
            routing_key='sensorgnome',
        )