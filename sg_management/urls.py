from django.urls import path, include
from sg_management import views

app_name = 'sg_management'

urlpatterns = [
                path('status/', views.StatusView.as_view()),
                path('detail/<slug:slug>', views.SingleDetailView.as_view(), name='serial'),
            ]