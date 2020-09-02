from django.contrib import admin
import user_management.models as models


admin.site.register(models.SensorgnomeUser)
admin.site.register(models.LocalUser)
admin.site.register(models.MotusUser)
admin.site.register(models.MotusPermissions)