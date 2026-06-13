<<<<<<< HEAD
=======

import logging
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f
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
<<<<<<< HEAD
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                status=400,
            )
        except Exception:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "An unexpected error occurred",
                },
                status=500,
            )

=======
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
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f
    return wrapper
