from .celery import app as sensorgnome_server

# Needed to ensure celery is always imported when Django starts.
__all__ = ('sensorgnome_server',)