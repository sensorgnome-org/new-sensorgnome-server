from django.urls import path, include
from sg_management import views

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'sg_management'

urlpatterns = [
                path('status/', views.StatusView.as_view()),
                path('detail/<slug:slug>', views.SingleDetailView.as_view(), name='serial'),
                path('apiv0/link/<str:serial>', views.link_motus_receiver)
            ]