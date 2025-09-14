from django.apps import AppConfig

class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"

    def ready(self):
        # import signals to ensure they attach
        from . import signals  # noqa
