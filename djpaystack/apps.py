from django.apps import AppConfig
from django.core.checks import Error, register


class DjPaystackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djpaystack'
    verbose_name = 'DJ Paystack'

    def ready(self):
        """Import signals and register checks when app is ready"""
        try:
            import djpaystack.signals  # noqa
        except ImportError:
            pass

        _register_paystack_checks()


def _register_paystack_checks():
    """Register Django system checks for Paystack configuration."""

    @register('djpaystack')
    def check_paystack_config(app_configs, **kwargs):
        from django.conf import settings as django_settings

        errors = []
        paystack_conf = getattr(django_settings, 'PAYSTACK', {})

        if not paystack_conf.get('SECRET_KEY'):
            errors.append(
                Error(
                    "PAYSTACK['SECRET_KEY'] is not configured.",
                    hint="Add PAYSTACK = {'SECRET_KEY': 'sk_...'} to your Django settings.",
                    id='djpaystack.E001',
                )
            )

        return errors
