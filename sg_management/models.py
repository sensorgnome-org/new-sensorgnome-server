from django.contrib.gis.db import models
import uuid
from datetime import datetime, timezone
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
        self.last_seen = datetime.now(timezone.utc)
        self.save()


class MotusSensorgnome(models.Model):
    """
    Stores Motus metadata associated with a SensorGnome.
    """

    class Status(models.IntegerChoices):
        ACTIVE = 0, "active"
        PENDING = 1, "pending"
        TERMINATED = 2, "terminated"

    class RcvType(models.IntegerChoices):
        OTHER = 0, "Other"
        ACTIVE = 1, "Sensorgnome"
        PENDING = 2, "Lotek"
        TERMINATED = 3, "SensorStation"

    # RECEIVER_TYPE_CHOICES = [(0, "Sensorgnome"), (1, "Lotek"), (2, "SensorStation"), (3, "Other")]
    # RECEIVER_STATUS_CHOICES = [(0, "active"), (1, "pending"), (2, "terminated")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.IntegerField(blank=True, null=True)
    deployment_name = models.TextField(blank=True, null=True)
    deployment_status = models.IntegerField(choices=Status.choices)
    motus_receiver_id = models.IntegerField()
    project_receiver_id = models.IntegerField()
    deployment_start = models.DateTimeField(blank=True, null=True)
    receiver_type = models.IntegerField(choices=RcvType.choices)
    receiver_id = models.CharField(max_length=20, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)

    def __str__(self):
        receiver_type = self.RcvType.choices[self.receiver_type][1]
        status = self.Status.choices[self.deployment_status][1]
        return f"Motus Receiver: {self.motus_receiver_id} device {self.device_id} is a {receiver_type} with status {status}."

    def receiver_from_api(self, parent_sensorgnome):
        """
        Creates a instance of this model given a SensorGnome model and links them together.
        If already linked to a SensorGnome model, updates existing model.
        Args:
            parent_sensorgnome (SensorGnome): A Sensorgnome to add Motus metadata for.
        """
        motus = motus_api.SGMotusAPI()
        res = motus.get_receiver(parent_sensorgnome.serial)
        if not res:
            return None, False
        kwargs = {"device_id": res.device_id,}
        defaults = {
                "deployment_name": res.deployment_name,
                "deployment_status": [a[0] for a in self.Status.choices if res.deployment_status.lower() == a[1].lower()][0],
                "motus_receiver_id": res.motus_receiver_id,
                "project_receiver_id": res.project_receiver_id,
                "deployment_start": res.deployment_start,
                "receiver_type": res.receiver_type,
                "receiver_id": res.receiver_id,
                "mac_address": res.mac_address,
        }
        receiver_type = [a[0] for a in self.RcvType.choices if defaults["receiver_type"].lower() == a[1].lower()][0]
        if not receiver_type:
            receiver_type = self.RcvType.choices[0][0]
        defaults["receiver_type"] = receiver_type
        obj, created = MotusSensorgnome.objects.update_or_create(**kwargs, defaults=defaults)
        print("obj:", obj, created)
        parent_sensorgnome.motus_metadata = obj
        parent_sensorgnome.save()
        return obj, created