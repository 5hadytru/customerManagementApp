from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # overriding ready method
    def ready(self):
        from . import signals
