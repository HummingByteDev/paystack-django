"""
Configuration settings for paystack-django
"""

from typing import Any, Dict, Optional

from django.conf import settings

from .exceptions import PaystackConfigurationError


class PaystackSettings:
    """
    Central configuration manager for Paystack settings
    """

    DEFAULTS: Dict[str, Any] = {
        "SECRET_KEY": None,
        "PUBLIC_KEY": None,
        "BASE_URL": "https://api.paystack.co",
        "TIMEOUT": 30,
        "MAX_RETRIES": 3,
        "VERIFY_SSL": True,
        # Paystack signs webhooks with the account SECRET_KEY. WEBHOOK_SECRET is
        # therefore an *override* that defaults to SECRET_KEY (see
        # ``webhook_secret`` below). Leave as None to use SECRET_KEY.
        "WEBHOOK_SECRET": None,
        # when True (default) webhooks without a verifiable signature are
        # rejected. Set False only for local development.
        "WEBHOOK_SIGNATURE_REQUIRED": True,
        "CALLBACK_URL": None,
        "CURRENCY": "NGN",
        "ENVIRONMENT": "production",  # 'production' or 'test'
        "AUTO_VERIFY_TRANSACTIONS": True,
        "CACHE_TIMEOUT": 300,  # 5 minutes
        "LOG_REQUESTS": False,
        "LOG_RESPONSES": False,
        "ENABLE_SIGNALS": True,
        "ENABLE_MODELS": True,
        "ALLOWED_WEBHOOK_IPS": [],
    }

    def __init__(self) -> None:
        self._settings: Optional[Dict[str, Any]] = None

    def _load_settings(self) -> None:
        """Load settings from Django settings"""
        if self._settings is not None:
            return

        user_settings = getattr(settings, "PAYSTACK", {})
        self._settings = {**self.DEFAULTS, **user_settings}

        # Validate required settings
        if not self._settings.get("SECRET_KEY"):
            raise PaystackConfigurationError(
                "PAYSTACK['SECRET_KEY'] is required in Django settings"
            )

    def __getattr__(self, name: str) -> Any:
        self._load_settings()
        assert self._settings is not None
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value with optional default"""
        self._load_settings()
        assert self._settings is not None
        return self._settings.get(key, default)  # type: ignore[return-value]

    @property
    def webhook_secret(self) -> Optional[str]:
        """Resolve the webhook signing secret.

        Paystack signs webhooks using the account SECRET_KEY, so an explicit
        ``WEBHOOK_SECRET`` is treated as an override and falls back to
        ``SECRET_KEY`` when not set.
        """
        self._load_settings()
        assert self._settings is not None
        return self._settings.get("WEBHOOK_SECRET") or self._settings.get("SECRET_KEY")

    def reload(self) -> None:
        """Reload settings from Django settings"""
        self._settings = None
        self._load_settings()


paystack_settings = PaystackSettings()
