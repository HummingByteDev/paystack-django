"""
Regression tests for Paystack API request and webhook compliance.

Each test asserts the exact wire contract (verb, path, params/json) the SDK
sends against the official Paystack OpenAPI specification, so parity bugs
cannot silently regress.
"""

from unittest.mock import Mock, patch

import pytest

from djpaystack import PaystackClient
from djpaystack.webhooks.events import WebhookEvent


@pytest.fixture
def client():
    with patch("djpaystack.client.paystack_settings") as s:
        s.SECRET_KEY = "sk_test_xxxxx"
        s.BASE_URL = "https://api.paystack.co"
        s.TIMEOUT = 30
        s.MAX_RETRIES = 3
        s.VERIFY_SSL = True
        yield PaystackClient()


def _mock_ok(client):
    """Patch the session and return the mock for call inspection."""
    mock_request = patch.object(client.session, "request").start()
    resp = Mock()
    resp.json.return_value = {"status": True, "message": "ok", "data": []}
    resp.status_code = 200
    mock_request.return_value = resp
    return mock_request


class TestDateFilterMapping:
    """from_date/to_date must be sent as wire names from/to."""

    def test_transactions_list_maps_dates(self, client):
        mock_request = _mock_ok(client)
        try:
            client.transactions.list(from_date="2026-01-01", to_date="2026-02-01", page=1)
            _, kwargs = mock_request.call_args
            params = kwargs["params"]
            assert params.get("from") == "2026-01-01"
            assert params.get("to") == "2026-02-01"
            assert "from_date" not in params
            assert "to_date" not in params
        finally:
            patch.stopall()

    def test_customers_list_maps_dates(self, client):
        mock_request = _mock_ok(client)
        try:
            client.customers.list(from_date="2026-01-01", to_date="2026-02-01", page=1)
            _, kwargs = mock_request.call_args
            params = kwargs["params"]
            assert params.get("from") == "2026-01-01"
            assert params.get("to") == "2026-02-01"
        finally:
            patch.stopall()


class TestTransfersRecipientFilter:
    """list filter is `recipient` (with `customer` as legacy alias)."""

    def test_recipient_param(self, client):
        mock_request = _mock_ok(client)
        try:
            client.transfers.list(recipient=42, page=1)
            _, kwargs = mock_request.call_args
            assert kwargs["params"].get("recipient") == 42
            assert "customer" not in kwargs["params"]
        finally:
            patch.stopall()

    def test_customer_alias_maps_to_recipient(self, client):
        mock_request = _mock_ok(client)
        try:
            client.transfers.list(customer=42, page=1)
            _, kwargs = mock_request.call_args
            assert kwargs["params"].get("recipient") == 42
        finally:
            patch.stopall()


class TestBulkChargePauseResume:
    """pause/resume are GET /bulkcharge/{pause,resume}/{code}."""

    def test_pause(self, client):
        mock_request = _mock_ok(client)
        try:
            client.bulk_charges.pause("BCH_xxx")
            args, kwargs = mock_request.call_args
            assert kwargs["method"] == "GET"
            assert args[0] == "GET" if args else kwargs["method"] == "GET"
            assert kwargs["url"].endswith("/bulkcharge/pause/BCH_xxx")
        finally:
            patch.stopall()

    def test_resume(self, client):
        mock_request = _mock_ok(client)
        try:
            client.bulk_charges.resume("BCH_xxx")
            _, kwargs = mock_request.call_args
            assert kwargs["method"] == "GET"
            assert kwargs["url"].endswith("/bulkcharge/resume/BCH_xxx")
        finally:
            patch.stopall()


class TestChargeSubmitAddress:
    """submit_address must send zip_code, not zipcode."""

    def test_zip_code_key(self, client):
        mock_request = _mock_ok(client)
        try:
            client.charge.submit_address(
                address="1 St",
                reference="ref",
                city="Lagos",
                state="LA",
                zipcode="100001",
            )
            _, kwargs = mock_request.call_args
            body = kwargs["json"]
            assert body.get("zip_code") == "100001"
            assert "zipcode" not in body
        finally:
            patch.stopall()


class TestWebhookEventNames:
    """dispute events are charge.dispute.*, refund.processing exists."""

    def test_dispute_event_values(self):
        assert WebhookEvent.DISPUTE_CREATE.value == "charge.dispute.create"
        assert WebhookEvent.DISPUTE_REMIND.value == "charge.dispute.remind"
        assert WebhookEvent.DISPUTE_RESOLVE.value == "charge.dispute.resolve"

    def test_dispute_events_are_valid(self):
        assert WebhookEvent.is_valid("charge.dispute.create")
        assert WebhookEvent.is_valid("charge.dispute.resolve")

    def test_refund_processing_present(self):
        assert WebhookEvent.is_valid("refund.processing")


def test_dispute_create_event_dispatches_handler_and_signal():
    """a real `charge.dispute.create` event now reaches the handler
    and fires the `paystack_dispute_created` signal (previously never executed)."""
    from djpaystack.signals import paystack_dispute_created
    from djpaystack.webhooks.handlers import WebhookHandler

    received = []

    def receiver(sender, **kwargs):
        received.append(kwargs.get("dispute_data"))

    paystack_dispute_created.connect(receiver)
    try:
        with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
            s.ENABLE_MODELS = False
            s.ENABLE_SIGNALS = True
            handler = WebhookHandler()
            handler.handle_event("charge.dispute.create", {"id": "DSP_1"})
        assert received == [{"id": "DSP_1"}]
    finally:
        paystack_dispute_created.disconnect(receiver)


@pytest.mark.django_db
def test_transfer_reversed_records_reversed_status():
    """a reversed transfer is recorded as 'reversed', not 'failed'."""
    from djpaystack.models import PaystackTransfer
    from djpaystack.webhooks.handlers import WebhookHandler

    PaystackTransfer.objects.create(
        transfer_code="TRF_x",
        reference="r1",
        amount=1000,
        status="success",
        recipient_code="RCP_x",
    )
    with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
        s.ENABLE_MODELS = True
        s.ENABLE_SIGNALS = False
        WebhookHandler().handle_transfer_reversed({"transfer_code": "TRF_x"})

    assert PaystackTransfer.objects.get(transfer_code="TRF_x").status == "reversed"
