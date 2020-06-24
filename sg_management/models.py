from django.contrib.gis.db import models
import uuid
import datetime
import motus_api

class SensorGnome(models.Model):
    """
    This model represents a SensorGnome and its state.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial = models.CharField(max_length=20, verbose_name="Serial Number", unique=True)
    name = models.CharField(max_length=256)
    last_seen = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    motus_metadata = models.ForeignKey('MotusSensorgnome', blank=True, null=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Sensorgnome"
        verbose_name_plural = "Sensorgnomes"

    def __str__(self):
        return f"{self.serial}/{self.name}: {self.last_seen}"

    def update_last_seen(self):
        self.last_seen = datetime.datetime.utcnow()
        self.save()

class MotusSensorgnome(models.Model):
    """
    Stores Motus metadata associated with a SensorGnome.
    """
    RECEIVER_TYPE_CHOICES = [(0, "Sensorgnome"), (1, "Lotek"), (2, "SensorStation"), (3, "Other")]

    device_id = models.IntegerField(primary_key=True)
    deployment_name = models.TextField()
    deployment_status = models.BooleanField()
    motus_receiver_id = models.IntegerField()
    project_receiver_id = models.IntegerField()
    deployment_start = models.DateTimeField()
    receiver_type = models.IntegerField(choices=RECEIVER_TYPE_CHOICES)
    receiver_id = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return f"Motus Receiver: {self.motus_receiver_id} device {self.device_id} is a {self.receiver_type}."

    def receiver_from_api(self, sensorgnome):
        """
        Creates a instance of this model given a SensorGnome model and links them together.
        If already linked to a SensorGnome model, updates existing model.
        Args:
            sensorgnome (SensorGnome): A Sensorgnome to add Motus metadata for.
        """
        motus = motus_api.SGMotusAPI()
        res = motus.get_receiver(sensorgnome.serial)
        print(res)