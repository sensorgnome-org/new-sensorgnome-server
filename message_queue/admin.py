from django.contrib import admin
import message_queue.models as models

# Register your models here.

admin.site.register(models.Message)