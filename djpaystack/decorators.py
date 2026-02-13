
from functools import wraps
from django.http import JsonResponse
from .exceptions import PaystackError


def handle_paystack_errors(func):
    """
    Decorator to handle Paystack errors in views
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PaystackError as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred',
            }, status=500)
    return wrapper
