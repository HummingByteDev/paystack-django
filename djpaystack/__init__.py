"""
paystack-django: A complete Django integration for Paystack Payment Gateway
"""

from .client import PaystackClient
from .exceptions import (
    PaystackAPIError,
    PaystackAuthenticationError,
    PaystackError,
    PaystackNetworkError,
    PaystackValidationError,
)

__version__ = "2.0.0"
__author__ = "Humming Byte"
__email__ = "dev@hummingbyte.org"
__license__ = "MIT"

# ``default_app_config`` was deprecated in Django 3.2 and removed in
# Django 4.1. The AppConfig is discovered automatically from apps.py.


__all__ = [
    "PaystackClient",
    "PaystackError",
    "PaystackAPIError",
    "PaystackValidationError",
    "PaystackAuthenticationError",
    "PaystackNetworkError",
]
