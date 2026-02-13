"""
Custom exceptions for paystack-django
"""


class PaystackError(Exception):
    """Base exception for all Paystack errors"""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class PaystackAPIError(PaystackError):
    """Raised when Paystack API returns an error response"""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message, response)
        self.status_code = status_code


class PaystackValidationError(PaystackError):
    """Raised when request data validation fails"""
    pass


class PaystackAuthenticationError(PaystackError):
    """Raised when authentication with Paystack fails"""
    pass


class PaystackNetworkError(PaystackError):
    """Raised when network request to Paystack fails"""
    pass


class PaystackWebhookError(PaystackError):
    """Raised when webhook validation or processing fails"""
    pass


class PaystackConfigurationError(PaystackError):
    """Raised when configuration is invalid or missing"""
    pass
