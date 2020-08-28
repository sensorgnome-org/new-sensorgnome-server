import pytest
from .models import SensorgnomeUser, MotusUser, MotusPermissions, LocalUser


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

    @pytest.mark.django_db
    def test_local_user_creation(self):
        test_username = "Golden Plover"
        test_password = "f5+F[xjR;ph@G9Ct"  # This is only for testing and is NOT used anywhere in the project.
        local_user = LocalUser()
        local_user.create_local_user(test_username, test_password)
        assert local_user.user.username == test_username
        # The database should be storing the hashed password, but it is possible to bypass this. Make sure this hasn't happened.
        assert local_user.user.password != test_password