<<<<<<< HEAD
# Create your views here.
=======
"""
Views for Paystack integration.

Provides a base callback view for handling Paystack payment redirects.
Subclass PaystackCallbackView and override on_success / on_failure
to customise behaviour.
"""
import logging

from django.http import JsonResponse
from django.views import View

from .client import PaystackClient
from .exceptions import PaystackError

logger = logging.getLogger('djpaystack')


class PaystackCallbackView(View):
    """
    Handle Paystack payment callback (redirect after payment).

    Override ``on_success`` and ``on_failure`` in a subclass to customise
    behaviour for your application.
    """

    def get(self, request, *args, **kwargs):
        """Handle GET callback from Paystack redirect"""
        reference = request.GET.get('reference') or request.GET.get('trxref')
        if not reference:
            return JsonResponse(
                {'status': 'error', 'message': 'Missing transaction reference'},
                status=400,
            )

        try:
            client = PaystackClient()
            response = client.transactions.verify(reference)
            data = response.get('data', {})

            if data.get('status') == 'success':
                return self.on_success(request, reference, data)
            return self.on_failure(request, reference, data)
        except PaystackError as e:
            logger.error(
                "Callback verification failed for %s: %s", reference, e)
            return self.on_failure(request, reference, {'error': str(e)})

    def on_success(self, request, reference, data):
        """Handle successful payment – override in subclass."""
        return JsonResponse({'status': 'success', 'reference': reference, 'data': data})

    def on_failure(self, request, reference, data):
        """Handle failed payment – override in subclass."""
        return JsonResponse(
            {'status': 'failed', 'reference': reference, 'data': data}, status=400
        )
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f
