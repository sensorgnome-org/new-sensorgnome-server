from django.urls import path
from sg_management import views

app_name = 'sg_management'

urlpatterns = [path('status/', views.StatusView.as_view()),]