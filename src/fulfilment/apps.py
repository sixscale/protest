from django.apps import AppConfig


class FulfilmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fulfilment'

    def ready(self):
        from .scheduler import scheduler
        scheduler.start()
