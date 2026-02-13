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
        if request.path.startswith('/paystack/webhook'):
            logger.info(
                f"Paystack webhook request: {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')}"
            )
        return None
