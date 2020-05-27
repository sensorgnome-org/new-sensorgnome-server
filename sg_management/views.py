from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from sg_management.models import SensorGnome

class StatusView(ListView):
    model = SensorGnome

