from rest_framework import serializers

from .models import SensorGnome, MotusSensorgnome

class MotusReceiverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MotusSensorgnome
        fields = ['device_id', 'deployment_name', 'deployment_status', 'motus_receiver_id', 'project_receiver_id', 'deployment_start', 'receiver_type', 'receiver_id', 'mac_address']