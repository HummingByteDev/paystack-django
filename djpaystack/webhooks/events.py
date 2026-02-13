
from enum import Enum
from typing import Dict, Any


class WebhookEvent(str, Enum):
    """
    Paystack webhook event types
    https://paystack.com/docs/payments/webhooks/
    """

    # Charge Events
    CHARGE_SUCCESS = 'charge.success'
    CHARGE_FAILED = 'charge.failed'

    # Transfer Events
    TRANSFER_SUCCESS = 'transfer.success'
    TRANSFER_FAILED = 'transfer.failed'
    TRANSFER_REVERSED = 'transfer.reversed'

    # Subscription Events
    SUBSCRIPTION_CREATE = 'subscription.create'
    SUBSCRIPTION_DISABLE = 'subscription.disable'
    SUBSCRIPTION_NOT_RENEW = 'subscription.not_renew'
    SUBSCRIPTION_EXPIRING_CARDS = 'subscription.expiring_cards'

    # Invoice Events
    INVOICE_CREATE = 'invoice.create'
    INVOICE_UPDATE = 'invoice.update'
    INVOICE_PAYMENT_FAILED = 'invoice.payment_failed'

    # Customer Events
    CUSTOMERIDENTIFICATION_SUCCESS = 'customeridentification.success'
    CUSTOMERIDENTIFICATION_FAILED = 'customeridentification.failed'

    # Refund Events
    REFUND_PENDING = 'refund.pending'
    REFUND_PROCESSED = 'refund.processed'
    REFUND_FAILED = 'refund.failed'

    # Dispute Events
    DISPUTE_CREATE = 'dispute.create'
    DISPUTE_REMIND = 'dispute.remind'
    DISPUTE_RESOLVE = 'dispute.resolve'

    # Dedicated Account Events
    DEDICATEDACCOUNT_ASSIGN_SUCCESS = 'dedicatedaccount.assign.success'
    DEDICATEDACCOUNT_ASSIGN_FAILED = 'dedicatedaccount.assign.failed'

    # Payment Request Events
    PAYMENTREQUEST_PENDING = 'paymentrequest.pending'
    PAYMENTREQUEST_SUCCESS = 'paymentrequest.success'

    # Product Events
    PRODUCTORDER_PENDING = 'productorder.pending'
    PRODUCTORDER_SUCCESS = 'productorder.success'

    # Terminal Events
    TERMINAL_LIVE = 'terminal.live'
    TERMINAL_OFFLINE = 'terminal.offline'

    @classmethod
    def all_events(cls) -> list:
        """Get all webhook event types"""
        return [event.value for event in cls]

    @classmethod
    def is_valid(cls, event: str) -> bool:
        """Check if event type is valid"""
        return event in cls.all_events()


class WebhookEventData:
    """
    Data structure for webhook events
    """

    def __init__(self, event: str, data: Dict[str, Any]):
        self.event = event
        self.data = data
        self.event_id = self._generate_event_id()

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        # Try to get ID from various fields
        if 'id' in self.data:
            return f"{self.event}_{self.data['id']}"
        elif 'reference' in self.data:
            return f"{self.event}_{self.data['reference']}"
        elif 'transfer_code' in self.data:
            return f"{self.event}_{self.data['transfer_code']}"
        else:
            import uuid
            return f"{self.event}_{uuid.uuid4().hex[:12]}"

    @property
    def reference(self) -> str:
        """Get transaction reference"""
        return self.data.get('reference', '')

    @property
    def amount(self) -> int:
        """Get transaction amount"""
        return self.data.get('amount', 0)

    @property
    def currency(self) -> str:
        """Get currency"""
        return self.data.get('currency', 'NGN')

    @property
    def customer(self) -> Dict[str, Any]:
        """Get customer data"""
        return self.data.get('customer', {})

    @property
    def customer_email(self) -> str:
        """Get customer email"""
        return self.customer.get('email', '')

    @property
    def customer_code(self) -> str:
        """Get customer code"""
        return self.customer.get('customer_code', '')

    @property
    def status(self) -> str:
        """Get status"""
        return self.data.get('status', '')

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata"""
        return self.data.get('metadata', {})
