
import logging
from collections import OrderedDict
from typing import Dict, Any, Callable, Optional

from ..settings import paystack_settings
from ..exceptions import PaystackWebhookError
from ..utils import verify_webhook_signature
from .events import WebhookEvent, WebhookEventData
from ..signals import (
    paystack_payment_successful,
    paystack_payment_failed,
    paystack_subscription_created,
    paystack_subscription_cancelled,
    paystack_transfer_successful,
    paystack_transfer_failed,
    paystack_refund_processed,
    paystack_dispute_created,
    paystack_dispute_resolved,
)

logger = logging.getLogger('djpaystack')


# Paystack webhook IPs for whitelisting
PAYSTACK_WEBHOOK_IPS = [
    '52.31.139.75',
    '52.49.173.169',
    '52.214.14.220',
]


class WebhookHandler:
    """
    Enhanced webhook handler for Paystack events

    Features:
    - Event type validation
    - IP whitelisting
    - Signature verification
    - Automatic retry handling
    - Event deduplication
    """

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._register_default_handlers()
        self._processed_events: OrderedDict = OrderedDict()

    def _register_default_handlers(self):
        """Register default event handlers"""
        # Charge events
        self.register(WebhookEvent.CHARGE_SUCCESS, self.handle_charge_success)
        self.register(WebhookEvent.CHARGE_FAILED, self.handle_charge_failed)

        # Transfer events
        self.register(WebhookEvent.TRANSFER_SUCCESS,
                      self.handle_transfer_success)
        self.register(WebhookEvent.TRANSFER_FAILED,
                      self.handle_transfer_failed)
        self.register(WebhookEvent.TRANSFER_REVERSED,
                      self.handle_transfer_reversed)

        # Subscription events
        self.register(WebhookEvent.SUBSCRIPTION_CREATE,
                      self.handle_subscription_create)
        self.register(WebhookEvent.SUBSCRIPTION_DISABLE,
                      self.handle_subscription_disable)
        self.register(WebhookEvent.SUBSCRIPTION_NOT_RENEW,
                      self.handle_subscription_not_renew)

        # Refund events
        self.register(WebhookEvent.REFUND_PROCESSED,
                      self.handle_refund_processed)

        # Dispute events
        self.register(WebhookEvent.CHARGE_DISPUTE_CREATE,
                      self.handle_dispute_create)
        self.register(WebhookEvent.CHARGE_DISPUTE_RESOLVE,
                      self.handle_dispute_resolve)

        # Dedicated Account events
        self.register(WebhookEvent.DEDICATEDACCOUNT_ASSIGN_SUCCESS,
                      self.handle_dva_assign_success)

        # Invoice events
        self.register(WebhookEvent.INVOICE_CREATE, self.handle_invoice_create)
        self.register(WebhookEvent.INVOICE_PAYMENT_FAILED,
                      self.handle_invoice_failed)

    def register(self, event_type: str, handler: Callable):
        """
        Register a handler for an event type

        Args:
            event_type: Event type (use WebhookEvent enum)
            handler: Callable to handle the event
        """
        self._handlers[event_type] = handler
        logger.info("Registered webhook handler for %s", event_type)

    def verify_ip(self, ip_address: str) -> bool:
        """
        Verify that request comes from Paystack IP

        Args:
            ip_address: Request IP address

        Returns:
            True if IP is whitelisted
        """
        allowed_ips = paystack_settings.ALLOWED_WEBHOOK_IPS

        # If no IPs configured, allow Paystack default IPs
        if not allowed_ips:
            allowed_ips = PAYSTACK_WEBHOOK_IPS

        # If list is empty, allow all (not recommended for production)
        if not allowed_ips:
            logger.warning(
                "No webhook IP whitelist configured - allowing all IPs")
            return True

        return ip_address in allowed_ips

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify webhook signature using HMAC SHA512

        Args:
            payload: Raw request body
            signature: X-Paystack-Signature header value

        Returns:
            True if signature is valid
        """
        webhook_secret = paystack_settings.WEBHOOK_SECRET
        if not webhook_secret:
            logger.error(
                "WEBHOOK_SECRET not configured - rejecting webhook request. "
                "Set PAYSTACK['WEBHOOK_SECRET'] in your Django settings."
            )
            return False

        return verify_webhook_signature(payload, signature, webhook_secret)

    def is_duplicate_event(self, event_id: str) -> bool:
        """
        Check if event has already been processed (for idempotency)

        Args:
            event_id: Unique event identifier

        Returns:
            True if event was already processed
        """
        if event_id in self._processed_events:
            return True

        # Also check database if models are enabled
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackWebhookEvent
            return PaystackWebhookEvent.objects.filter(event_id=event_id).exists()

        return False

    def mark_event_processed(self, event_id: str):
        """Mark event as processed"""
        self._processed_events[event_id] = True

        # Limit in-memory cache size (evict oldest entries)
        while len(self._processed_events) > 1000:
            self._processed_events.popitem(last=False)

    def handle_event(self, event_type: str, data: Dict[str, Any]) -> Any:
        """
        Handle a webhook event

        Args:
            event_type: Event type
            data: Event data

        Returns:
            Handler result

        Raises:
            PaystackWebhookError: If handler fails
        """
        # Validate event type
        if not WebhookEvent.is_valid(event_type):
            logger.warning("Unknown webhook event type: %s", event_type)
            return None

        # Create event data object
        event_data = WebhookEventData(event_type, data)

        # Check for duplicate
        if self.is_duplicate_event(event_data.event_id):
            logger.info("Duplicate event detected: %s - skipping",
                        event_data.event_id)
            return {'status': 'duplicate', 'message': 'Event already processed'}

        handler = self._handlers.get(event_type)

        if not handler:
            logger.warning(
                "No handler registered for event type: %s", event_type)
            return None

        try:
            logger.info("Processing webhook event: %s", event_type)
            result = handler(data)

            # Mark as processed
            self.mark_event_processed(event_data.event_id)

            logger.info("Successfully processed webhook event: %s", event_type)
            return result
        except Exception as e:
            logger.error("Error handling webhook event %s: %s",
                         event_type, e, exc_info=True)
            raise PaystackWebhookError(
                f"Failed to handle webhook event: {str(e)}")

    # Default event handlers

    def handle_charge_success(self, data: Dict[str, Any]):
        """Handle successful charge"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackTransaction

            reference = data.get('reference')
            if reference:
                PaystackTransaction.objects.update_or_create(
                    reference=reference,
                    defaults={
                        'amount': data.get('amount'),
                        'currency': data.get('currency', 'NGN'),
                        'status': 'success',
                        'customer_email': data.get('customer', {}).get('email'),
                        'customer_code': data.get('customer', {}).get('customer_code'),
                        'authorization_code': data.get('authorization', {}).get('authorization_code'),
                        'channel': data.get('channel'),
                        'fees': data.get('fees'),
                        'paid_at': data.get('paid_at'),
                        'metadata': data.get('metadata'),
                        'raw_response': data,
                    }
                )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_payment_successful.send(
                sender=self.__class__,
                transaction_data=data
            )

    def handle_charge_failed(self, data: Dict[str, Any]):
        """Handle failed charge"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackTransaction

            reference = data.get('reference')
            if reference:
                PaystackTransaction.objects.update_or_create(
                    reference=reference,
                    defaults={
                        'amount': data.get('amount'),
                        'currency': data.get('currency', 'NGN'),
                        'status': 'failed',
                        'customer_email': data.get('customer', {}).get('email'),
                        'customer_code': data.get('customer', {}).get('customer_code'),
                        'metadata': data.get('metadata'),
                        'raw_response': data,
                    }
                )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_payment_failed.send(
                sender=self.__class__,
                transaction_data=data
            )

    def handle_subscription_create(self, data: Dict[str, Any]):
        """Handle subscription creation"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackSubscription

            subscription_code = data.get('subscription_code')
            if subscription_code:
                PaystackSubscription.objects.update_or_create(
                    subscription_code=subscription_code,
                    defaults={
                        'customer_code': data.get('customer', {}).get('customer_code'),
                        'plan_code': data.get('plan', {}).get('plan_code'),
                        'amount': data.get('amount'),
                        'status': data.get('status', 'active'),
                        'next_payment_date': data.get('next_payment_date'),
                        'authorization_code': data.get('authorization', {}).get('authorization_code'),
                        'metadata': data.get('metadata'),
                        'raw_response': data,
                    }
                )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_subscription_created.send(
                sender=self.__class__,
                subscription_data=data
            )

    def handle_subscription_disable(self, data: Dict[str, Any]):
        """Handle subscription cancellation"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackSubscription

            subscription_code = data.get('subscription_code')
            if subscription_code:
                PaystackSubscription.objects.filter(
                    subscription_code=subscription_code
                ).update(status='cancelled')

        if paystack_settings.ENABLE_SIGNALS:
            paystack_subscription_cancelled.send(
                sender=self.__class__,
                subscription_data=data
            )

    def handle_subscription_not_renew(self, data: Dict[str, Any]):
        """Handle subscription that will not renew"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackSubscription

            subscription_code = data.get('subscription_code')
            if subscription_code:
                PaystackSubscription.objects.filter(
                    subscription_code=subscription_code
                ).update(status='non-renewing')

    def handle_transfer_success(self, data: Dict[str, Any]):
        """Handle successful transfer"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackTransfer

            transfer_code = data.get('transfer_code')
            if transfer_code:
                PaystackTransfer.objects.update_or_create(
                    transfer_code=transfer_code,
                    defaults={
                        'reference': data.get('reference'),
                        'amount': data.get('amount'),
                        'currency': data.get('currency', 'NGN'),
                        'status': 'success',
                        'recipient_code': data.get('recipient', {}).get('recipient_code'),
                        'reason': data.get('reason'),
                        'transferred_at': data.get('transferred_at'),
                        'metadata': data.get('metadata'),
                        'raw_response': data,
                    }
                )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_transfer_successful.send(
                sender=self.__class__,
                transfer_data=data
            )

    def handle_transfer_failed(self, data: Dict[str, Any]):
        """Handle failed transfer"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackTransfer

            transfer_code = data.get('transfer_code')
            if transfer_code:
                PaystackTransfer.objects.update_or_create(
                    transfer_code=transfer_code,
                    defaults={
                        'reference': data.get('reference'),
                        'amount': data.get('amount'),
                        'currency': data.get('currency', 'NGN'),
                        'status': 'failed',
                        'recipient_code': data.get('recipient', {}).get('recipient_code'),
                        'reason': data.get('reason'),
                        'metadata': data.get('metadata'),
                        'raw_response': data,
                    }
                )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_transfer_failed.send(
                sender=self.__class__,
                transfer_data=data
            )

    def handle_transfer_reversed(self, data: Dict[str, Any]):
        """Handle reversed transfer"""
        if paystack_settings.ENABLE_MODELS:
            from ..models import PaystackTransfer

            transfer_code = data.get('transfer_code')
            if transfer_code:
                PaystackTransfer.objects.filter(
                    transfer_code=transfer_code
                ).update(
                    status='failed',
                    raw_response=data
                )

    def handle_refund_processed(self, data: Dict[str, Any]):
        """Handle processed refund"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_refund_processed.send(
                sender=self.__class__,
                refund_data=data
            )

    def handle_dispute_create(self, data: Dict[str, Any]):
        """Handle dispute creation"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_dispute_created.send(
                sender=self.__class__,
                dispute_data=data
            )

    def handle_dispute_resolve(self, data: Dict[str, Any]):
        """Handle dispute resolution"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_dispute_resolved.send(
                sender=self.__class__,
                dispute_data=data
            )

    def handle_dva_assign_success(self, data: Dict[str, Any]):
        """Handle successful dedicated account assignment"""
        logger.info("Dedicated account assigned: %s",
                    data.get('account_number'))

    def handle_invoice_create(self, data: Dict[str, Any]):
        """Handle invoice creation"""
        logger.info("Invoice created: %s", data.get('reference'))

    def handle_invoice_failed(self, data: Dict[str, Any]):
        """Handle failed invoice payment"""
        logger.warning("Invoice payment failed: %s", data.get('reference'))


# Global webhook handler instance
webhook_handler = WebhookHandler()
