from django.contrib.gis.db import models
import uuid

# Create your models here.

class Exchange(models.Model):
    """
    This model represents a rabbitmq AMQP exchange.
    """
    type_choices = [(1, "direct"), (2, "fanout"), (3, "headers"), (4, "topic")]

    name = models.CharField(max_length=128, primary_key=True)
    ex_type = models.IntegerField(choices=type_choices, default=1)
    durable = models.BooleanField(default=True)

    def __str__(self):
        return f"Exchange: {self.name}, type: {self.ex_type}, durable: {self.durable}."

class Queue(models.Model):
    """
    This model represnets a rabbitmq AMQP queue.
    """
    type_choices = [(1, "classic"), (2, "quorum")]

    name = models.CharField(max_length=128, primary_key=True)
    q_type = models.IntegerField(choices=type_choices, default=1)
    durable = models.BooleanField(default=True)

    def __str__(self):
        return f"Queue: {self.name}, type: {self.q_type}, durable: {self.durable}."

class Message(models.Model):
    """
    This model is for storing messages received by the server.
    This is pretty much just a test model right now.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    payload = models.TextField()

    def __str__(self):
        return f"{self.timestamp}: \"{self.payload}\""