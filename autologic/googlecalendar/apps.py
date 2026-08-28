from django.apps import AppConfig


class GooglecalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'googlecalendar'
    verbose_name = 'Integración Google Calendar'

    def ready(self):
        from . import signals  # noqa: F401 - registra los receivers de señales
