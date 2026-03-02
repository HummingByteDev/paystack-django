
import logging
from collections import OrderedDict
from typing import Dict, Any, Callable, Optional

from ..settings import paystack_settings
from ..exceptions import PaystackWebhookError
from ..utils import verify_webhook_signature
from .events import WebhookEvent, WebhookEventData
from ..signals import (
    paystack_payment_successful,
    paystack_subscription_created,
    paystack_subscription_cancelled,
    paystack_subscription_not_renewing,
    paystack_subscription_expiring_cards,
    paystack_transfer_successful,
    paystack_transfer_failed,
    paystack_transfer_reversed,
    paystack_refund_pending,
    paystack_refund_processing,
    paystack_refund_processed,
    paystack_refund_failed,
    paystack_dispute_created,
    paystack_dispute_remind,
    paystack_dispute_resolved,
    paystack_customeridentification_success,
    paystack_customeridentification_failed,
    paystack_dedicatedaccount_assign_success,
    paystack_dedicatedaccount_assign_failed,
    paystack_invoice_created,
    paystack_invoice_updated,
    paystack_invoice_payment_failed,
    paystack_paymentrequest_pending,
    paystack_paymentrequest_success,
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
        """Register default event handlers for all supported Paystack events"""
        # Charge events
        self.register(WebhookEvent.CHARGE_SUCCESS, self.handle_charge_success)

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
        self.register(WebhookEvent.SUBSCRIPTION_EXPIRING_CARDS,
                      self.handle_subscription_expiring_cards)

        # Refund events
        self.register(WebhookEvent.REFUND_PENDING,
                      self.handle_refund_pending)
        self.register(WebhookEvent.REFUND_PROCESSING,
                      self.handle_refund_processing)
        self.register(WebhookEvent.REFUND_PROCESSED,
                      self.handle_refund_processed)
        self.register(WebhookEvent.REFUND_FAILED,
                      self.handle_refund_failed)

        # Dispute events
        self.register(WebhookEvent.CHARGE_DISPUTE_CREATE,
                      self.handle_dispute_create)
        self.register(WebhookEvent.CHARGE_DISPUTE_REMIND,
                      self.handle_dispute_remind)
        self.register(WebhookEvent.CHARGE_DISPUTE_RESOLVE,
                      self.handle_dispute_resolve)

        # Customer Identification events
        self.register(WebhookEvent.CUSTOMERIDENTIFICATION_SUCCESS,
                      self.handle_customeridentification_success)
        self.register(WebhookEvent.CUSTOMERIDENTIFICATION_FAILED,
                      self.handle_customeridentification_failed)

        # Dedicated Account events
        self.register(WebhookEvent.DEDICATEDACCOUNT_ASSIGN_SUCCESS,
                      self.handle_dva_assign_success)
        self.register(WebhookEvent.DEDICATEDACCOUNT_ASSIGN_FAILED,
                      self.handle_dva_assign_failed)

        # Invoice events
        self.register(WebhookEvent.INVOICE_CREATE, self.handle_invoice_create)
        self.register(WebhookEvent.INVOICE_UPDATE, self.handle_invoice_update)
        self.register(WebhookEvent.INVOICE_PAYMENT_FAILED,
                      self.handle_invoice_payment_failed)

        # Payment Request events
        self.register(WebhookEvent.PAYMENTREQUEST_PENDING,
                      self.handle_paymentrequest_pending)
        self.register(WebhookEvent.PAYMENTREQUEST_SUCCESS,
                      self.handle_paymentrequest_success)

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
        Verify webhook signature using HMAC SHA512.

        Paystack signs webhooks with your API secret key (``PAYSTACK['SECRET_KEY']``).
        No separate webhook secret is needed.

        Args:
            payload: Raw request body
            signature: X-Paystack-Signature header value

        Returns:
            True if signature is valid
        """
        secret_key = paystack_settings.SECRET_KEY
        if not secret_key:
            logger.error(
                "SECRET_KEY not configured - rejecting webhook request. "
                "Set PAYSTACK['SECRET_KEY'] in your Django settings."
            )
            return False

        return verify_webhook_signature(payload, signature, secret_key)

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

    # ------------------------------------------------------------------
    # Default event handlers
    # ------------------------------------------------------------------

    # --- Charge events ------------------------------------------------

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
                data=data
            )

    # --- Subscription events ------------------------------------------

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
                data=data
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
                data=data
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

        if paystack_settings.ENABLE_SIGNALS:
            paystack_subscription_not_renewing.send(
                sender=self.__class__,
                data=data
            )

    def handle_subscription_expiring_cards(self, data: Dict[str, Any]):
        """Handle notification of expiring cards on subscriptions"""
        logger.info(
            "Expiring cards notification received for %d subscriptions",
            len(data) if isinstance(data, list) else 1,
        )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_subscription_expiring_cards.send(
                sender=self.__class__,
                data=data
            )

    # --- Transfer events ----------------------------------------------

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
                data=data
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
                data=data
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

        if paystack_settings.ENABLE_SIGNALS:
            paystack_transfer_reversed.send(
                sender=self.__class__,
                data=data
            )

    # --- Refund events ------------------------------------------------

    def handle_refund_pending(self, data: Dict[str, Any]):
        """Handle pending refund"""
        logger.info("Refund pending: transaction %s", data.get('transaction'))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_refund_pending.send(
                sender=self.__class__,
                data=data
            )

    def handle_refund_processing(self, data: Dict[str, Any]):
        """Handle refund that is being processed"""
        logger.info("Refund processing: transaction %s",
                    data.get('transaction'))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_refund_processing.send(
                sender=self.__class__,
                data=data
            )

    def handle_refund_processed(self, data: Dict[str, Any]):
        """Handle processed refund"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_refund_processed.send(
                sender=self.__class__,
                data=data
            )

    def handle_refund_failed(self, data: Dict[str, Any]):
        """Handle failed refund"""
        logger.warning("Refund failed: transaction %s",
                       data.get('transaction'))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_refund_failed.send(
                sender=self.__class__,
                data=data
            )

    # --- Dispute events -----------------------------------------------

    def handle_dispute_create(self, data: Dict[str, Any]):
        """Handle dispute creation"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_dispute_created.send(
                sender=self.__class__,
                data=data
            )

    def handle_dispute_remind(self, data: Dict[str, Any]):
        """Handle dispute reminder"""
        logger.info("Dispute reminder: %s", data.get('id'))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_dispute_remind.send(
                sender=self.__class__,
                data=data
            )

    def handle_dispute_resolve(self, data: Dict[str, Any]):
        """Handle dispute resolution"""
        if paystack_settings.ENABLE_SIGNALS:
            paystack_dispute_resolved.send(
                sender=self.__class__,
                data=data
            )

    # --- Customer Identification events -------------------------------

    def handle_customeridentification_success(self, data: Dict[str, Any]):
        """Handle successful customer identification (BVN/NIN)"""
        logger.info(
            "Customer identification succeeded: %s",
            data.get('customer_code', data.get('customer_id')),
        )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_customeridentification_success.send(
                sender=self.__class__,
                data=data
            )

    def handle_customeridentification_failed(self, data: Dict[str, Any]):
        """Handle failed customer identification"""
        logger.warning(
            "Customer identification failed: %s",
            data.get('customer_code', data.get('customer_id')),
        )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_customeridentification_failed.send(
                sender=self.__class__,
                data=data
            )

    # --- Dedicated Account events -------------------------------------

    def handle_dva_assign_success(self, data: Dict[str, Any]):
        """Handle successful dedicated account assignment"""
        logger.info("Dedicated account assigned: %s",
                    data.get('dedicated_account', {}).get('account_number',
                                                          data.get('account_number')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_dedicatedaccount_assign_success.send(
                sender=self.__class__,
                data=data
            )

    def handle_dva_assign_failed(self, data: Dict[str, Any]):
        """Handle failed dedicated account assignment"""
        logger.warning(
            "Dedicated account assignment failed: %s",
            data.get('customer', {}).get('customer_code'),
        )

        if paystack_settings.ENABLE_SIGNALS:
            paystack_dedicatedaccount_assign_failed.send(
                sender=self.__class__,
                data=data
            )

    # --- Invoice events -----------------------------------------------

    def handle_invoice_create(self, data: Dict[str, Any]):
        """Handle invoice creation"""
        logger.info("Invoice created: %s", data.get('invoice_code',
                                                    data.get('reference')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_invoice_created.send(
                sender=self.__class__,
                data=data
            )

    def handle_invoice_update(self, data: Dict[str, Any]):
        """Handle invoice update"""
        logger.info("Invoice updated: %s", data.get('invoice_code',
                                                    data.get('reference')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_invoice_updated.send(
                sender=self.__class__,
                data=data
            )

    def handle_invoice_payment_failed(self, data: Dict[str, Any]):
        """Handle failed invoice payment"""
        logger.warning("Invoice payment failed: %s", data.get('invoice_code',
                                                              data.get('reference')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_invoice_payment_failed.send(
                sender=self.__class__,
                data=data
            )

    # --- Payment Request events ---------------------------------------

    def handle_paymentrequest_pending(self, data: Dict[str, Any]):
        """Handle pending payment request"""
        logger.info("Payment request pending: %s", data.get('request_code',
                                                            data.get('id')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_paymentrequest_pending.send(
                sender=self.__class__,
                data=data
            )

    def handle_paymentrequest_success(self, data: Dict[str, Any]):
        """Handle successful payment request"""
        logger.info("Payment request succeeded: %s", data.get('request_code',
                                                              data.get('id')))

        if paystack_settings.ENABLE_SIGNALS:
            paystack_paymentrequest_success.send(
                sender=self.__class__,
                data=data
            )


# Global webhook handler instance
webhook_handler = WebhookHandler()
