from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView
from sg_management.models import SensorGnome, MotusSensorgnome

from sg_management.serializers import MotusReceiverSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

class StatusView(ListView):
    model = SensorGnome

class SingleDetailView(DetailView):
    model = SensorGnome
    slug_field = "serial"

class MotusReceiver(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = MotusSensorgnome.objects.all()
    serializer_class = MotusReceiverSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

@api_view(['GET'])
def link_motus_receiver(request, serial):
    """
    Links a Sensorgnome with a Motus Receiver.
    """
    created = False
    try:
        sg = SensorGnome.objects.get(serial=serial)
        motus_receiver = MotusSensorgnome()
        res, created = motus_receiver.receiver_from_api(sg)
        serializer = MotusReceiverSerializer(res)
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    except SensorGnome.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
