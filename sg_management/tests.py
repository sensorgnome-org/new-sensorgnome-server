from django.test import TestCase
from .models import SensorGnome, MotusSensorgnome
from datetime import datetime


class SensorGnomeTestCase(TestCase):
    def setup(self):

        # Create a SG that isn't in Motus.
        serial = "SG-424242424242"
        name = "Test Sensorgnome"
        last_seen = datetime.utcnow()
        notes = "Testing creation of a Sensorgnome."
        SensorGnome.objects.create(serial=serial, name=name, last_seen=last_seen, notes=notes)
        # This SG should be in Motus.
        serial = "SG-F28CRPI33503"
        name = "Physical Sensorgnome"
        last_seen = datetime.utcnow()
        notes = "Testing creation of a Sensorgnome."
        SensorGnome.objects.create(serial=serial, name=name, last_seen=last_seen, notes=notes)

    def test_motus_link_new(self):
        serial = "SG-F28CRPI33503"
        motus_receiver = MotusSensorgnome()
        res, created = motus_receiver.receiver_from_api(serial)
        assert created == True