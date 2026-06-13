
import pytest
from unittest.mock import patch, MagicMock
from djpaystack.settings import PaystackSettings


class TestPaystackSettings:
    """Test PaystackSettings configuration manager"""

    def test_loads_defaults(self):
        """Test that defaults are loaded correctly"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_xxx'}

            settings = PaystackSettings()
            assert settings.SECRET_KEY == 'sk_test_xxx'
            assert settings.BASE_URL == 'https://api.paystack.co'
            assert settings.TIMEOUT == 30
            assert settings.MAX_RETRIES == 3

    def test_user_settings_override_defaults(self):
        """Test that user settings override defaults"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {
                'SECRET_KEY': 'sk_test_xxx',
                'TIMEOUT': 60,
                'CURRENCY': 'USD',
            }

            settings = PaystackSettings()
            assert settings.TIMEOUT == 60
            assert settings.CURRENCY == 'USD'

    def test_missing_secret_key_raises(self):
        """Test that missing SECRET_KEY raises ConfigurationError"""
        from djpaystack.exceptions import PaystackConfigurationError

        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {}

            settings = PaystackSettings()
            with pytest.raises(PaystackConfigurationError):
                _ = settings.SECRET_KEY

    def test_invalid_attribute_raises(self):
        """Test that accessing non-existent setting raises AttributeError"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_xxx'}

            settings = PaystackSettings()
            with pytest.raises(AttributeError):
                _ = settings.NON_EXISTENT_SETTING

    def test_get_method_with_default(self):
        """Test get() method returns default for missing keys"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_xxx'}

            settings = PaystackSettings()
            assert settings.get('NON_EXISTENT', 'fallback') == 'fallback'

    def test_get_method_returns_value(self):
        """Test get() method returns setting value when present"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_xxx'}

            settings = PaystackSettings()
            assert settings.get('SECRET_KEY') == 'sk_test_xxx'

    def test_reload_reloads_from_django(self):
        """Test reload() picks up changed Django settings"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_old'}

            settings = PaystackSettings()
            assert settings.SECRET_KEY == 'sk_test_old'

            # Change Django settings and reload
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_new'}
            settings.reload()
            assert settings.SECRET_KEY == 'sk_test_new'

    def test_lazy_loading(self):
        """Test settings are loaded lazily (only on first access)"""
        with patch('djpaystack.settings.settings') as mock_django:
            mock_django.PAYSTACK = {'SECRET_KEY': 'sk_test_xxx'}

            settings = PaystackSettings()
            # Internal _settings should be None before first access
            assert settings._settings is None

            # After access, should be loaded
            _ = settings.SECRET_KEY
            assert settings._settings is not None
