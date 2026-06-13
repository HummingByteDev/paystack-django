"""
Tests for the production-hardening changes:

  * pagination no longer eagerly loads all pages; iter_all streams.
  * webhook deduplication is DB-backed and race-safe.
  * 401/403 map to PaystackAuthenticationError.
  * ISO datetime strings are parsed before ORM assignment.
"""

import hashlib
import hmac
import json
from unittest.mock import Mock, patch

from django.test import RequestFactory, TestCase

import pytest

from djpaystack import PaystackClient
from djpaystack.exceptions import PaystackAuthenticationError


def _client():
    with patch("djpaystack.client.paystack_settings") as s:
        s.SECRET_KEY = "sk_test_xxxxx"
        s.BASE_URL = "https://api.paystack.co"
        s.TIMEOUT = 30
        s.MAX_RETRIES = 3
        s.VERIFY_SSL = True
        return PaystackClient()


# --------------------------------------------------------------------------- #
# pagination
# --------------------------------------------------------------------------- #
class TestPaginationSafety:
    def test_list_fetches_single_page_only(self):
        client = _client()
        mock_request = patch.object(client.session, "request").start()
        try:
            resp = Mock()
            resp.status_code = 200
            resp.json.return_value = {
                "status": True,
                "message": "ok",
                "data": [{"id": 1}],
                "meta": {"page": 1, "pageCount": 5},  # 5 pages exist...
            }
            mock_request.return_value = resp

            out = client.transactions.list()  # no page arg
            # ...but only ONE request is made, and meta is preserved.
            assert mock_request.call_count == 1
            assert out["meta"]["pageCount"] == 5
            _, kwargs = mock_request.call_args
            assert kwargs["params"]["page"] == 1
        finally:
            patch.stopall()

    def test_iter_all_streams_all_pages_lazily(self):
        client = _client()
        mock_request = patch.object(client.session, "request").start()
        try:
            pages = [
                {
                    "status": True,
                    "data": [{"id": 1}, {"id": 2}],
                    "meta": {"page": 1, "pageCount": 2},
                },
                {"status": True, "data": [{"id": 3}], "meta": {"page": 2, "pageCount": 2}},
            ]
            responses = []
            for body in pages:
                r = Mock()
                r.status_code = 200
                r.json.return_value = body
                responses.append(r)
            mock_request.side_effect = responses

            ids = [item["id"] for item in client.transactions.iter_all()]
            assert ids == [1, 2, 3]
            assert mock_request.call_count == 2
        finally:
            patch.stopall()


# --------------------------------------------------------------------------- #
# error mapping
# --------------------------------------------------------------------------- #
class TestErrorMapping:
    def test_401_maps_to_authentication_error(self):
        client = _client()
        mock_request = patch.object(client.session, "request").start()
        try:
            resp = Mock()
            resp.status_code = 401
            resp.json.return_value = {"status": False, "message": "Invalid key"}
            mock_request.return_value = resp
            with pytest.raises(PaystackAuthenticationError):
                client.transactions.verify("ref")
        finally:
            patch.stopall()


# --------------------------------------------------------------------------- #
# webhook dedup (DB-backed, race-safe)
# --------------------------------------------------------------------------- #
class TestWebhookDeduplication(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        from djpaystack.webhooks.views import PaystackWebhookView

        self.view = PaystackWebhookView.as_view()
        self.secret = "test_webhook_secret"

    def _signed_request(self):
        payload = {
            "event": "charge.success",
            "data": {
                "reference": "dup_ref_1",
                "amount": 1000,
                "currency": "NGN",
                "customer": {"email": "a@b.com"},
            },
        }
        body = json.dumps(payload).encode()
        sig = hmac.new(self.secret.encode(), body, hashlib.sha512).hexdigest()
        return self.factory.post(
            "/webhook/", data=body, content_type="application/json", HTTP_X_PAYSTACK_SIGNATURE=sig
        )

    def test_duplicate_delivery_processed_once(self):
        from djpaystack.models import PaystackWebhookEvent

        with patch("djpaystack.webhooks.handlers.webhook_handler.handle_event") as handle, patch(
            "djpaystack.webhooks.views.paystack_settings"
        ) as vs, patch("djpaystack.webhooks.handlers.paystack_settings") as hs:
            vs.ENABLE_MODELS = True
            hs.webhook_secret = self.secret
            hs.WEBHOOK_SIGNATURE_REQUIRED = True

            r1 = self.view(self._signed_request())
            r2 = self.view(self._signed_request())

            assert r1.status_code == 200
            assert r2.status_code == 200
            # Handler invoked exactly once despite two identical deliveries.
            assert handle.call_count == 1
            # Exactly one stored event row.
            assert (
                PaystackWebhookEvent.objects.filter(event_id="charge.success_dup_ref_1").count()
                == 1
            )


# --------------------------------------------------------------------------- #
# datetime parsing
# --------------------------------------------------------------------------- #
@pytest.mark.django_db
def test_charge_success_parses_paid_at():
    from djpaystack.models import PaystackTransaction
    from djpaystack.webhooks.handlers import WebhookHandler

    with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
        s.ENABLE_MODELS = True
        s.ENABLE_SIGNALS = False
        WebhookHandler().handle_charge_success(
            {
                "reference": "r_dt",
                "amount": 1000,
                "currency": "NGN",
                "customer": {"email": "a@b.com"},
                "paid_at": "2026-01-15T12:00:00.000Z",
            }
        )
    txn = PaystackTransaction.objects.get(reference="r_dt")
    # Stored as an actual datetime, not a string.
    assert txn.paid_at is not None
    assert txn.paid_at.year == 2026
