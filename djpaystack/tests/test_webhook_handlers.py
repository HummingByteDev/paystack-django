"""
Tests for all Paystack webhook event handlers.

Verifies that every supported event type:
1. Has a registered handler
2. Dispatches the correct Django signal (when ENABLE_SIGNALS=True)
3. Does not raise exceptions on valid data
"""

from unittest.mock import patch, MagicMock

from django.test import TestCase

from djpaystack.webhooks.events import WebhookEvent
from djpaystack.webhooks.handlers import WebhookHandler


# ---------------------------------------------------------------------------
# Sample payloads (minimal but realistic)
# ---------------------------------------------------------------------------

_CHARGE_DATA = {
    'reference': 'ref_test_001',
    'amount': 50000,
    'currency': 'NGN',
    'status': 'success',
    'channel': 'card',
    'fees': 750,
    'paid_at': '2025-01-15T12:00:00.000Z',
    'customer': {'email': 'test@example.com', 'customer_code': 'CUS_xxx'},
    'authorization': {'authorization_code': 'AUTH_xxx'},
    'metadata': {},
}

_SUBSCRIPTION_DATA = {
    'subscription_code': 'SUB_xxx',
    'customer': {'email': 'test@example.com', 'customer_code': 'CUS_xxx'},
    'plan': {'plan_code': 'PLN_xxx', 'name': 'Pro', 'amount': 500000, 'interval': 'monthly'},
    'amount': 500000,
    'status': 'active',
    'next_payment_date': '2025-02-15T00:00:00.000Z',
    'authorization': {'authorization_code': 'AUTH_xxx'},
    'metadata': {},
}

_TRANSFER_DATA = {
    'transfer_code': 'TRF_xxx',
    'reference': 'trf_ref_001',
    'amount': 100000,
    'currency': 'NGN',
    'status': 'success',
    'recipient': {'recipient_code': 'RCP_xxx', 'type': 'nuban', 'name': 'Recipient'},
    'reason': 'Test',
    'transferred_at': '2025-01-15T12:00:00.000Z',
    'metadata': {},
}

_REFUND_DATA = {
    'id': 334455,
    'transaction': 987654,
    'amount': 50000,
    'currency': 'NGN',
    'status': 'processed',
    'refunded_at': '2025-01-15T12:00:00.000Z',
}

_DISPUTE_DATA = {
    'id': 556677,
    'status': 'awaiting-merchant-feedback',
    'amount': 50000,
    'currency': 'NGN',
    'transaction': {'id': 987654, 'reference': 'txn_abc', 'amount': 50000},
    'category': 'general',
    'message': 'Dispute test',
}

_CUSTOMERID_DATA = {
    'customer_id': 123456,
    'customer_code': 'CUS_xxx',
    'email': 'test@example.com',
    'identification': {'country': 'NG', 'type': 'bvn', 'value': '22012345678'},
    'reason': '',
}

_DVA_DATA = {
    'customer': {'email': 'test@example.com', 'customer_code': 'CUS_xxx'},
    'dedicated_account': {
        'account_name': 'PAYSTACK-Test',
        'account_number': '0000000000',
        'bank': {'name': 'Wema Bank', 'id': 20},
        'id': 55555,
    },
}

_INVOICE_DATA = {
    'id': 667788,
    'invoice_code': 'INV_xxx',
    'reference': 'inv_ref_001',
    'amount': 50000,
    'currency': 'NGN',
    'status': 'pending',
    'customer': {'email': 'test@example.com', 'customer_code': 'CUS_xxx'},
    'description': 'Monthly subscription',
}

_PAYMENTREQUEST_DATA = {
    'id': 889900,
    'request_code': 'PRQ_xxx',
    'amount': 50000,
    'currency': 'NGN',
    'status': 'pending',
    'customer': {'email': 'test@example.com', 'customer_code': 'CUS_xxx'},
    'description': 'Test payment request',
}


# ---------------------------------------------------------------------------
# Mapping: every required event → (sample data, expected signal name)
# ---------------------------------------------------------------------------

_EVENT_TABLE = [
    # -- Charge --
    (WebhookEvent.CHARGE_SUCCESS,  _CHARGE_DATA, 'paystack_payment_successful'),
    # -- Dispute --
    (WebhookEvent.CHARGE_DISPUTE_CREATE,  _DISPUTE_DATA, 'paystack_dispute_created'),
    (WebhookEvent.CHARGE_DISPUTE_REMIND,  _DISPUTE_DATA, 'paystack_dispute_remind'),
    (WebhookEvent.CHARGE_DISPUTE_RESOLVE,
     _DISPUTE_DATA, 'paystack_dispute_resolved'),
    # -- Customer identification --
    (WebhookEvent.CUSTOMERIDENTIFICATION_SUCCESS,
     _CUSTOMERID_DATA, 'paystack_customeridentification_success'),
    (WebhookEvent.CUSTOMERIDENTIFICATION_FAILED,  {
     **_CUSTOMERID_DATA, 'reason': 'Not verified'}, 'paystack_customeridentification_failed'),
    # -- Dedicated account --
    (WebhookEvent.DEDICATEDACCOUNT_ASSIGN_SUCCESS,
     _DVA_DATA, 'paystack_dedicatedaccount_assign_success'),
    (WebhookEvent.DEDICATEDACCOUNT_ASSIGN_FAILED,
     _DVA_DATA, 'paystack_dedicatedaccount_assign_failed'),
    # -- Invoice --
    (WebhookEvent.INVOICE_CREATE,          _INVOICE_DATA, 'paystack_invoice_created'),
    (WebhookEvent.INVOICE_UPDATE,          _INVOICE_DATA, 'paystack_invoice_updated'),
    (WebhookEvent.INVOICE_PAYMENT_FAILED,
     _INVOICE_DATA, 'paystack_invoice_payment_failed'),
    # -- Payment request --
    (WebhookEvent.PAYMENTREQUEST_PENDING,
     _PAYMENTREQUEST_DATA, 'paystack_paymentrequest_pending'),
    (WebhookEvent.PAYMENTREQUEST_SUCCESS, {
     **_PAYMENTREQUEST_DATA, 'status': 'success'}, 'paystack_paymentrequest_success'),
    # -- Refund --
    (WebhookEvent.REFUND_PENDING,    {
     **_REFUND_DATA, 'status': 'pending'}, 'paystack_refund_pending'),
    (WebhookEvent.REFUND_PROCESSING, {
     **_REFUND_DATA, 'status': 'processing'}, 'paystack_refund_processing'),
    (WebhookEvent.REFUND_PROCESSED,  _REFUND_DATA, 'paystack_refund_processed'),
    (WebhookEvent.REFUND_FAILED,     {
     **_REFUND_DATA, 'status': 'failed'}, 'paystack_refund_failed'),
    # -- Subscription --
    (WebhookEvent.SUBSCRIPTION_CREATE,
     _SUBSCRIPTION_DATA, 'paystack_subscription_created'),
    (WebhookEvent.SUBSCRIPTION_DISABLE,        {
     **_SUBSCRIPTION_DATA, 'status': 'cancelled'}, 'paystack_subscription_cancelled'),
    (WebhookEvent.SUBSCRIPTION_NOT_RENEW,      {
     **_SUBSCRIPTION_DATA, 'status': 'non-renewing'}, 'paystack_subscription_not_renewing'),
    (WebhookEvent.SUBSCRIPTION_EXPIRING_CARDS,
     _SUBSCRIPTION_DATA, 'paystack_subscription_expiring_cards'),
    # -- Transfer --
    (WebhookEvent.TRANSFER_SUCCESS,  _TRANSFER_DATA, 'paystack_transfer_successful'),
    (WebhookEvent.TRANSFER_FAILED,   {
     **_TRANSFER_DATA, 'status': 'failed'}, 'paystack_transfer_failed'),
    (WebhookEvent.TRANSFER_REVERSED, {
     **_TRANSFER_DATA, 'status': 'reversed'}, 'paystack_transfer_reversed'),
]


class TestAllWebhookHandlersRegistered(TestCase):
    """Every required event type must have a registered handler."""

    REQUIRED_EVENTS = [
        'charge.success',
        'charge.dispute.create',
        'charge.dispute.remind',
        'charge.dispute.resolve',
        'customeridentification.success',
        'customeridentification.failed',
        'dedicatedaccount.assign.success',
        'dedicatedaccount.assign.failed',
        'invoice.create',
        'invoice.update',
        'invoice.payment_failed',
        'paymentrequest.pending',
        'paymentrequest.success',
        'refund.pending',
        'refund.processing',
        'refund.processed',
        'refund.failed',
        'subscription.create',
        'subscription.disable',
        'subscription.not_renew',
        'subscription.expiring_cards',
        'transfer.success',
        'transfer.failed',
        'transfer.reversed',
    ]

    def test_all_required_events_have_handlers(self):
        handler = WebhookHandler()
        missing = [
            ev for ev in self.REQUIRED_EVENTS
            if ev not in handler._handlers
        ]
        self.assertEqual(
            missing, [],
            f"Missing handlers for: {missing}",
        )


class TestWebhookHandlerDispatch(TestCase):
    """Each handler must run without error and fire its signal."""

    def setUp(self):
        self.handler = WebhookHandler()

    @patch('djpaystack.webhooks.handlers.paystack_settings')
    def test_handler_runs_and_fires_signal(self, mock_settings):
        """Parametrised over _EVENT_TABLE."""
        mock_settings.ENABLE_MODELS = False
        mock_settings.ENABLE_SIGNALS = True

        for event_enum, data, signal_name in _EVENT_TABLE:
            with self.subTest(event=event_enum.value):
                signal_module = 'djpaystack.signals'
                with patch(f'{signal_module}.{signal_name}') as mock_signal:
                    mock_signal.send = MagicMock()

                    # Patch the signal on the handler module too
                    with patch(
                        f'djpaystack.webhooks.handlers.{signal_name}',
                        mock_signal,
                    ):
                        result = self.handler._handlers[event_enum.value](data)

                    mock_signal.send.assert_called_once()
                    # Verify sender and data kwarg
                    call_kwargs = mock_signal.send.call_args
                    self.assertEqual(
                        call_kwargs[1]['sender'], WebhookHandler,
                    )
                    self.assertIn('data', call_kwargs[1])

    @patch('djpaystack.webhooks.handlers.paystack_settings')
    def test_handler_skips_signal_when_disabled(self, mock_settings):
        """When ENABLE_SIGNALS=False, no signal should fire."""
        mock_settings.ENABLE_MODELS = False
        mock_settings.ENABLE_SIGNALS = False

        for event_enum, data, signal_name in _EVENT_TABLE:
            with self.subTest(event=event_enum.value):
                with patch(
                    f'djpaystack.webhooks.handlers.{signal_name}',
                ) as mock_signal:
                    self.handler._handlers[event_enum.value](data)
                    mock_signal.send.assert_not_called()


class TestWebhookEventEnum(TestCase):
    """The WebhookEvent enum must contain all required events."""

    REQUIRED_EVENTS = [
        'charge.success',
        'charge.dispute.create',
        'charge.dispute.remind',
        'charge.dispute.resolve',
        'customeridentification.success',
        'customeridentification.failed',
        'dedicatedaccount.assign.success',
        'dedicatedaccount.assign.failed',
        'invoice.create',
        'invoice.update',
        'invoice.payment_failed',
        'paymentrequest.pending',
        'paymentrequest.success',
        'refund.pending',
        'refund.processing',
        'refund.processed',
        'refund.failed',
        'subscription.create',
        'subscription.disable',
        'subscription.not_renew',
        'subscription.expiring_cards',
        'transfer.success',
        'transfer.failed',
        'transfer.reversed',
    ]

    def test_all_required_events_in_enum(self):
        all_values = WebhookEvent.all_events()
        missing = [ev for ev in self.REQUIRED_EVENTS if ev not in all_values]
        self.assertEqual(
            missing, [], f"Missing from WebhookEvent enum: {missing}")

    def test_is_valid_for_all_required_events(self):
        for ev in self.REQUIRED_EVENTS:
            with self.subTest(event=ev):
                self.assertTrue(WebhookEvent.is_valid(ev))
