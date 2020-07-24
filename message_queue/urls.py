from django.urls import path
from message_queue import views

app_name = 'message_queue'

urlpatterns = [path('publish', views.test_pub_view, name='publish'),]