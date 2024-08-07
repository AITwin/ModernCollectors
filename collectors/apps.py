from django.apps import AppConfig


class SourcesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collectors"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
