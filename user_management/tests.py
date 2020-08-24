import pytest
from .models import SensorgnomeUser, MotusUser, MotusPermissions


class TestMotusReceivers:
    @pytest.mark.django_db
    def setup(self):
        pass


    @pytest.mark.django_db
    def test_motus_user_link(self):
        temp_motus_id = 42
        temp_motus_token = "73475CB40A568E8DA8A045CED110137E159F890AC4DA883B6B17DC651B3A8049"
        username = "Mx. Barred Owl"
        motus_user = MotusUser()
        created_user = motus_user.add_motus_user(username)
        assert created_user.user_name == username
        assert created_user.linked_external_user.motus_token == temp_motus_token
        assert created_user.linked_external_user.motus_id == temp_motus_id
