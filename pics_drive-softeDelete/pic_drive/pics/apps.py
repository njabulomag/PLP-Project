from django.apps import AppConfig


class PicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pics'
    
    def ready(self):
       import pics.signals
