import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..exceptions import PaystackWebhookError
from ..models import PaystackWebhookEvent
from ..settings import paystack_settings
from .events import WebhookEventData
from .handlers import webhook_handler

logger = logging.getLogger("djpaystack")


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_POST, name="dispatch")
class PaystackWebhookView(View):
    """
    View for handling Paystack webhooks
    """

    def post(self, request, *args, **kwargs):
        """Handle POST request from Paystack webhook"""

        # Get signature header
        signature = request.headers.get("X-Paystack-Signature")
        if not signature:
            logger.warning("Webhook request missing signature")
            return JsonResponse({"status": "error", "message": "Missing signature"}, status=400)

        # Verify signature
        if not webhook_handler.verify_signature(request.body, signature):
            logger.warning("Invalid webhook signature")
            return JsonResponse({"status": "error", "message": "Invalid signature"}, status=400)

        # Parse payload
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        event_type = payload.get("event")
        data = payload.get("data", {})

        if not event_type:
            logger.error("Webhook payload missing event type")
            return JsonResponse({"status": "error", "message": "Missing event type"}, status=400)

        # derive a single canonical event id (shared with the handler)
        # and use the database unique constraint as the authoritative, race-safe
        # deduplication arbiter when models are enabled.
        event_id = WebhookEventData(event_type, data).event_id

        webhook_event = None
        if paystack_settings.ENABLE_MODELS:
            webhook_event, created = self._store_event(request, event_type, event_id, payload)
            if not created:
                # Another delivery already created (and owns) this event.
                logger.info(f"Duplicate webhook ignored: {event_id}")
                return JsonResponse({"status": "success", "message": "duplicate"})

        # Handle event (only the creator of the row reaches here for a given id)
        try:
            webhook_handler.handle_event(event_type, data)

            if webhook_event:
                webhook_event.processed = True
                webhook_event.save(update_fields=["processed", "updated_at"])

            return JsonResponse({"status": "success"})

        except PaystackWebhookError as e:
            logger.error(f"Webhook handling error: {str(e)}")

            if webhook_event:
                webhook_event.processing_error = str(e)
                webhook_event.save(update_fields=["processing_error", "updated_at"])

            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    def _store_event(self, request, event_type, event_id, payload):
        """Atomically store the event, returning ``(event, created)``.

        ``created`` is ``True`` when this request created the row (and therefore
        owns processing). On a storage error we return ``(None, True)`` so the
        event is still processed rather than silently dropped.
        """
        try:
            with transaction.atomic():
                return PaystackWebhookEvent.objects.get_or_create(
                    event_id=event_id,
                    defaults={
                        "event_type": event_type,
                        "data": payload,
                        "ip_address": self._get_client_ip(request),
                        "user_agent": request.headers.get("User-Agent", ""),
                    },
                )
        except Exception as e:
            logger.error(f"Failed to store webhook event: {str(e)}")
            return None, True

    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
