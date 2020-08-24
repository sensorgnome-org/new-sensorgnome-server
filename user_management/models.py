from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
import uuid
from datetime import datetime, timezone

class SensorgnomeUser(models.Model):
    """
    This model represents a Sensorgnome user. For now, this is just a stub/skeleton, as only Motus users are supported.
    Why the messing around with GenericForeignKey? So that later this can support external accounts from more than just motus if needed, easily.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=256)
    last_seen = models.DateTimeField()
    linked_external_user_id = models.UUIDField(editable=False)
    linked_external_user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    linked_external_user = GenericForeignKey("linked_external_user_type", "linked_external_user_id")

    class Meta:
        verbose_name = "Sensorgnome User"
        verbose_name_plural = "Sensorgnome Users"

    def update_last_seen(self):
        self.last_seen = datetime.now(timezone.utc)
        self.save()

    def __str__(self):
        return f"{self.user_name} in linked to {self.linked_external_user} of type {self.linked_external_user_type}"


class MotusUser(models.Model):
    """
    For now, the only external user auth this supports. This will eventually likely subclass an ExternalModel class, or similar.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    motus_id = models.BigIntegerField()
    motus_token = models.CharField(max_length=256)
    expiry = models.DateTimeField(blank=True, null=True)
    permissions = models.ForeignKey('MotusPermissions', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Motus User"
        verbose_name_plural = "Motus Users"

    def add_motus_user(self, sg_username):
        """
        Adds a Morus user, and creates an associated Sensorgnome user.
        Args:
            sg_username (str): Username of the sensorgnome user. Doesn't need to be unique.
        Returns:
            The created Sensorgnome User instance.
        """
        motus_permissions = MotusPermissions()  # stub for now
        motus_permissions.save()

        # The following two (or three) lines will need to be replaced with a API call when that works.
        # Todo: unstub these once Motus API figured out.
        self.motus_id = 42
        self.motus_token = "73475CB40A568E8DA8A045CED110137E159F890AC4DA883B6B17DC651B3A8049"
        self.expiry = None

        self.save()
        content = ContentType.objects.get(app_label="user_management", model="motususer")
        sg_user = SensorgnomeUser(user_name=sg_username, linked_external_user_id=self.id, linked_external_user_type=content)
        sg_user.update_last_seen()
        sg_user.save()
        return sg_user


class MotusPermissions(models.Model):
    """
    Permissions for a specific user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployments = models.TextField()

    class Meta:
        verbose_name = "Motus Permissions"
        verbose_name_plural = "Motus Permissions"