from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.users"

    def ready(self):
        # Register signals for sync or auth actions
        import core.users.presentation.signals
