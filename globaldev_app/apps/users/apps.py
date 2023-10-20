from contextlib import suppress

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    verbose_name = "Users"

    def ready(self):
        with suppress(ImportError):
            from users import (  # noqa: F401 pylint: disable=import-outside-toplevel
                signals,
            )
