from django.apps import AppConfig


class NotificacionesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notificaciones"
    verbose_name = "Notificaciones"

    def ready(self):
        from . import signals  # noqa: F401 - registra los receivers de señales
