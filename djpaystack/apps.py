from django.apps import AppConfig


class DjPaystackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djpaystack'
    verbose_name = 'DJ Paystack'

    def ready(self):
        """Import signals when app is ready"""
        try:
            import djpaystack.signals  # noqa
        except ImportError:
            pass
