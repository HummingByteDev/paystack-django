"""
Configuration settings for paystack-django
"""
from django.conf import settings
from .exceptions import PaystackConfigurationError


class PaystackSettings:
    """
    Central configuration manager for Paystack settings
    """

    DEFAULTS = {
        'SECRET_KEY': None,
        'PUBLIC_KEY': None,
        'BASE_URL': 'https://api.paystack.co',
        'TIMEOUT': 30,
        'MAX_RETRIES': 3,
        'VERIFY_SSL': True,
        'WEBHOOK_SECRET': None,
        'CALLBACK_URL': None,
        'CURRENCY': 'NGN',
        'ENVIRONMENT': 'production',  # 'production' or 'test'
        'AUTO_VERIFY_TRANSACTIONS': True,
        'CACHE_TIMEOUT': 300,  # 5 minutes
        'LOG_REQUESTS': False,
        'LOG_RESPONSES': False,
        'ENABLE_SIGNALS': True,
        'ENABLE_MODELS': True,
        'ALLOWED_WEBHOOK_IPS': [],
    }

    def __init__(self):
        self._settings = None

    def _load_settings(self):
        """Load settings from Django settings"""
        if self._settings is not None:
            return

        user_settings = getattr(settings, 'PAYSTACK', {})
        self._settings = {**self.DEFAULTS, **user_settings}

        # Validate required settings
        if not self._settings.get('SECRET_KEY'):
            raise PaystackConfigurationError(
                "PAYSTACK['SECRET_KEY'] is required in Django settings"
            )

    def __getattr__(self, name):
        self._load_settings()
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'")

    def get(self, key, default=None):
        """Get a setting value with optional default"""
        self._load_settings()
        return self._settings.get(key, default)

    def reload(self):
        """Reload settings from Django settings"""
        self._settings = None
        self._load_settings()


paystack_settings = PaystackSettings()
