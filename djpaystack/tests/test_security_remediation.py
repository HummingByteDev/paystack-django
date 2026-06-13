"""
Tests for webhook and HTTP-client security behaviour.

Covers:
  * webhook signature verification fails closed when no secret
  * non-idempotent HTTP methods are not auto-retried
  * client IP extraction returns a value
  * a User-Agent identifying the SDK is sent
"""

import hashlib
import hmac
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from djpaystack import PaystackClient
from djpaystack.webhooks.handlers import WebhookHandler
from djpaystack.webhooks.views import PaystackWebhookView


class TestWebhookSignatureFailClosed(TestCase):
    """missing secret must reject, not accept."""

    def setUp(self):
        self.handler = WebhookHandler()
        self.payload = b'{"event": "charge.success", "data": {}}'

    def test_missing_secret_rejects_by_default(self):
        with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
            s.webhook_secret = None
            s.WEBHOOK_SIGNATURE_REQUIRED = True
            assert self.handler.verify_signature(self.payload, "anything") is False

    def test_missing_secret_can_be_bypassed_explicitly_for_dev(self):
        with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
            s.webhook_secret = None
            s.WEBHOOK_SIGNATURE_REQUIRED = False
            assert self.handler.verify_signature(self.payload, "anything") is True

    def test_valid_signature_accepted(self):
        secret = "sk_test_secret"
        sig = hmac.new(secret.encode(), self.payload, hashlib.sha512).hexdigest()
        with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
            s.webhook_secret = secret
            s.WEBHOOK_SIGNATURE_REQUIRED = True
            assert self.handler.verify_signature(self.payload, sig) is True

    def test_forged_signature_rejected(self):
        with patch("djpaystack.webhooks.handlers.paystack_settings") as s:
            s.webhook_secret = "sk_test_secret"
            s.WEBHOOK_SIGNATURE_REQUIRED = True
            assert self.handler.verify_signature(self.payload, "deadbeef") is False


class TestWebhookSecretAliasesSecretKey(TestCase):
    """WEBHOOK_SECRET defaults to SECRET_KEY (Paystack signs with SECRET_KEY)."""

    def test_falls_back_to_secret_key(self):
        from django.test import override_settings

        from djpaystack.settings import paystack_settings

        with override_settings(PAYSTACK={"SECRET_KEY": "sk_test_abc"}):
            paystack_settings.reload()
            assert paystack_settings.webhook_secret == "sk_test_abc"
        paystack_settings.reload()

    def test_explicit_override_wins(self):
        from django.test import override_settings

        from djpaystack.settings import paystack_settings

        with override_settings(
            PAYSTACK={"SECRET_KEY": "sk_test_abc", "WEBHOOK_SECRET": "override"}
        ):
            paystack_settings.reload()
            assert paystack_settings.webhook_secret == "override"
        paystack_settings.reload()


class TestRetryPolicy(TestCase):
    """POST/PUT must not be in the auto-retry allowlist."""

    def _client(self):
        with patch("djpaystack.client.paystack_settings") as s:
            s.SECRET_KEY = "sk_test_xxxxx"
            s.BASE_URL = "https://api.paystack.co"
            s.TIMEOUT = 30
            s.MAX_RETRIES = 3
            s.VERIFY_SSL = True
            return PaystackClient()

    def test_mutating_methods_not_retried(self):
        client = self._client()
        adapter = client.session.get_adapter("https://api.paystack.co")
        allowed = adapter.max_retries.allowed_methods
        assert "POST" not in allowed
        assert "PUT" not in allowed
        assert "GET" in allowed

    def test_user_agent_header_present(self):
        client = self._client()
        ua = client.session.headers.get("User-Agent", "")
        assert ua.startswith("paystack-django/")


class TestClientIpExtraction(TestCase):
    """_get_client_ip must return a value (was returning None)."""

    def setUp(self):
        self.view = PaystackWebhookView()
        self.factory = RequestFactory()

    def test_remote_addr(self):
        request = self.factory.post("/webhook/", REMOTE_ADDR="1.2.3.4")
        assert self.view._get_client_ip(request) == "1.2.3.4"

    def test_x_forwarded_for_first_hop(self):
        request = self.factory.post("/webhook/")
        request.META["HTTP_X_FORWARDED_FOR"] = "9.9.9.9, 10.0.0.1"
        assert self.view._get_client_ip(request) == "9.9.9.9"
