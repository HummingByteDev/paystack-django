import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View

from .handlers import webhook_handler
from ..models import PaystackWebhookEvent
from ..exceptions import PaystackWebhookError
from ..settings import paystack_settings

logger = logging.getLogger('djpaystack')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class PaystackWebhookView(View):
    """
    View for handling Paystack webhooks
    """

    def post(self, request, *args, **kwargs):
        """Handle POST request from Paystack webhook"""

        # Get signature header
        signature = request.headers.get('X-Paystack-Signature')
        if not signature:
            logger.warning("Webhook request missing signature")
            return JsonResponse({'status': 'error', 'message': 'Missing signature'}, status=400)

        # Verify signature
        if not webhook_handler.verify_signature(request.body, signature):
            logger.warning("Invalid webhook signature")
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)

        # Parse payload
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        event_type = payload.get('event')
        data = payload.get('data', {})

        if not event_type:
            logger.error("Webhook payload missing event type")
            return JsonResponse({'status': 'error', 'message': 'Missing event type'}, status=400)

        # Store webhook event if models are enabled
        webhook_event = None
        if paystack_settings.ENABLE_MODELS:
            try:
                webhook_event = PaystackWebhookEvent.objects.create(
                    event_type=event_type,
                    event_id=f"{event_type}_{data.get('reference', data.get('id', ''))}",
                    data=payload,
                    ip_address=self._get_client_ip(request),
                    user_agent=request.headers.get('User-Agent', ''),
                )
            except Exception as e:
                logger.error(f"Failed to store webhook event: {str(e)}")

        # Handle event
        try:
            webhook_handler.handle_event(event_type, data)

            if webhook_event:
                webhook_event.processed = True
                webhook_event.save()

            return JsonResponse({'status': 'success'})

        except PaystackWebhookError as e:
            logger.error(f"Webhook handling error: {str(e)}")

            if webhook_event:
                webhook_event.processing_error = str(e)
                webhook_event.save()

            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
