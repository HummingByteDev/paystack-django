
import pytest
import django
from django.conf import settings


def pytest_configure():
    """Configure Django for pytest"""
    settings.configure(
        SECRET_KEY='test-secret-key',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'djpaystack',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        PAYSTACK={
            'SECRET_KEY': 'sk_test_xxxxx',
            'WEBHOOK_SECRET': 'test_webhook_secret',
            'ENVIRONMENT': 'test',
            'ENABLE_MODELS': True,
            'ENABLE_SIGNALS': True,
        },
        USE_TZ=True,
    )
    django.setup()


@pytest.fixture
def mock_paystack_response():
    """Mock successful Paystack API response"""
    return {
        'status': True,
        'message': 'Success',
        'data': {
            'reference': 'test_ref_123',
            'amount': 50000,
            'currency': 'NGN',
            'status': 'success',
        }
    }


@pytest.fixture
def mock_transaction_data():
    """Mock transaction data"""
    return {
        'reference': 'test_ref_123',
        'amount': 50000,
        'currency': 'NGN',
        'status': 'success',
        'customer': {
            'email': 'test@example.com',
            'customer_code': 'CUS_xxxxx'
        },
        'authorization': {
            'authorization_code': 'AUTH_xxxxx'
        },
        'channel': 'card',
        'fees': 750,
        'paid_at': '2024-01-15T12:00:00.000Z',
        'metadata': {}
    }
