import logging
from django.utils.deprecation import MiddlewareMixin
from .settings import paystack_settings

logger = logging.getLogger('djpaystack')


class PaystackLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log Paystack-related requests
    """

    def process_request(self, request):
        """Log incoming requests to webhook endpoints"""
        if request.path.startswith('/webhooks/paystack'):
            logger.info(
                "Paystack webhook request: %s %s from %s",
                request.method, request.path,
                request.META.get('REMOTE_ADDR'),
            )
        return None
