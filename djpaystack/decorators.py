
import logging
from functools import wraps

from django.http import JsonResponse

from .exceptions import PaystackError

logger = logging.getLogger('djpaystack')


def handle_paystack_errors(func):
    """
    Decorator to handle Paystack errors in views
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PaystackError as e:
            logger.warning("Paystack error in %s: %s", func.__name__, e)
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=400)
        except Exception:
            logger.exception("Unexpected error in %s", func.__name__)
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred',
            }, status=500)
    return wrapper
