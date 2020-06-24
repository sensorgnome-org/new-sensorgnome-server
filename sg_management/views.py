from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView
from sg_management.models import SensorGnome

class StatusView(ListView):
    model = SensorGnome

class SingleDetailView(DetailView):
    model = SensorGnome
    slug_field = "serial"
