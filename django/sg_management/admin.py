from django.contrib import admin
import sg_management.models as models

# Register your models here.

class SensorGnomeAdmin(admin.ModelAdmin):
    list_display = ("id", "serial", "name", "last_seen", "notes")

admin.site.register(models.SensorGnome, SensorGnomeAdmin)
admin.site.register(models.MotusSensorgnome)