from django.contrib.gis.db import models
import uuid

class SensorGnome(models.Model):
    """
    This model represents a SensorGnome and its state.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial = models.CharField(max_length=20, verbose_name="Serial Number", unique=True)
    name = models.CharField(max_length=256)
    last_seen = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.serial}/{self.name}: {self.last_seen}"