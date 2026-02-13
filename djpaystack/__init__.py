"""
paystack-django: A complete Django integration for Paystack Payment Gateway
"""

from .exceptions import (
    PaystackError,
    PaystackAPIError,
    PaystackValidationError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)
from .client import PaystackClient
__version__ = '1.0.0'
__author__ = 'Humming Byte'
__email__ = 'dev@hummingbyte.org'
__license__ = 'MIT'

default_app_config = 'djpaystack.apps.DjPaystackConfig'


__all__ = [
    'PaystackClient',
    'PaystackError',
    'PaystackAPIError',
    'PaystackValidationError',
    'PaystackAuthenticationError',
    'PaystackNetworkError',
]
