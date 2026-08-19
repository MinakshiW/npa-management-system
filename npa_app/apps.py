from django.apps import AppConfig


class NpaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'npa_app'

    def ready(self):
        import npa_app.signals