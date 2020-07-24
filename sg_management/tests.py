import pytest
from .models import SensorGnome, MotusSensorgnome
from datetime import datetime, timezone
import vcr



class TestMotusReceivers:
    @pytest.mark.django_db
    def setup(self):
        # Create a SG that isn't in Motus.
        serial = "SG-424242424242"
        name = "Test Sensorgnome"
        last_seen = datetime.now(timezone.utc)
        notes = "Testing creation of a Sensorgnome."
        SensorGnome.objects.create(serial=serial, name=name, last_seen=last_seen, notes=notes)
        # This SG should be in Motus.
        serial = "SG-F28CRPI33503"
        name = "Physical Sensorgnome"
        last_seen = datetime.now(timezone.utc)
        notes = "Testing creation of a Sensorgnome."
        SensorGnome.objects.create(serial=serial, name=name, last_seen=last_seen, notes=notes)


    @vcr.use_cassette("test-fixtures/test_motus_link_new.yaml", match_on=['method', 'scheme', 'host', 'port', 'path'])
    @pytest.mark.django_db
    def test_motus_link_new(self):
        serial = "SG-F28CRPI33503"
        motus_receiver = MotusSensorgnome()
        sg = SensorGnome.objects.get(serial=serial)
        res, created = motus_receiver.receiver_from_api(sg)
        assert created == True
        assert res.receiver_id == serial

    @vcr.use_cassette("test-fixtures/test_motus_link_existing.yaml", match_on=['method', 'scheme', 'host', 'port', 'path'])
    @pytest.mark.django_db
    def test_motus_link_existing(self):
        serial = "SG-F28CRPI33503"
        motus_receiver = MotusSensorgnome()
        sg = SensorGnome.objects.get(serial=serial)
        _, _ = motus_receiver.receiver_from_api(sg)
        motus_receiver = MotusSensorgnome()
        sg = SensorGnome.objects.get(serial=serial)
        res, created = motus_receiver.receiver_from_api(sg)
        assert created == False
        assert res.receiver_id == serial

    @vcr.use_cassette("test-fixtures/test_motus_link_new.yaml", match_on=['method', 'scheme', 'host', 'port', 'path'])    
    @pytest.mark.django_db
    def test_motus_link_no_exist(self):
        serial = "SG-424242424242"
        motus_receiver = MotusSensorgnome()
        sg = SensorGnome.objects.get(serial=serial)
        res, created = motus_receiver.receiver_from_api(sg)
        assert res == None
        assert created == False