
import json
import hashlib
import hmac
from django.test import TestCase, RequestFactory
from djpaystack.webhooks.handlers import webhook_handler
from djpaystack.webhooks.events import WebhookEvent
from djpaystack.webhooks.views import PaystackWebhookView

from unittest.mock import patch


class TestWebhookHandler(TestCase):
    """Test webhook handler"""

    def setUp(self):
        self.handler = webhook_handler

    def test_signature_verification(self):
        """Test webhook signature verification"""
        payload = b'{"event": "charge.success", "data": {}}'
        secret = 'test_secret'

        # Generate valid signature
        signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()

        with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
            mock_settings.WEBHOOK_SECRET = secret

            result = self.handler.verify_signature(payload, signature)
            assert result is True

    def test_invalid_signature(self):
        """Test invalid signature rejection"""
        payload = b'{"event": "charge.success", "data": {}}'
        secret = 'test_secret'
        invalid_signature = 'invalid_signature'

        with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
            mock_settings.WEBHOOK_SECRET = secret

            result = self.handler.verify_signature(payload, invalid_signature)
            assert result is False

    def test_event_handling(self):
        """Test event handling"""
        data = {
            'reference': 'test_ref_123',
            'amount': 50000,
            'currency': 'NGN',
            'status': 'success',
            'customer': {
                'email': 'test@example.com',
                'customer_code': 'CUS_xxxxx'
            },
            'authorization': {
                'authorization_code': 'AUTH_xxxxx'
            },
            'channel': 'card',
            'fees': 750,
            'paid_at': '2024-01-15T12:00:00.000Z',
            'metadata': {}
        }

        with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
            mock_settings.ENABLE_MODELS = False
            mock_settings.ENABLE_SIGNALS = False

            result = self.handler.handle_event(
                WebhookEvent.CHARGE_SUCCESS,
                data
            )

            # Should not raise exception (handlers return None by design)
            assert result is None

    def test_duplicate_event_detection(self):
        """Test duplicate event detection"""
        event_id = 'test_event_123'

        # First call should not be duplicate
        assert self.handler.is_duplicate_event(event_id) is False

        # Mark as processed
        self.handler.mark_event_processed(event_id)

        # Second call should be duplicate
        assert self.handler.is_duplicate_event(event_id) is True


class TestWebhookView(TestCase):
    """Test webhook view"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = PaystackWebhookView.as_view()

    def test_missing_signature(self):
        """Test request without signature"""
        payload = {'event': 'charge.success', 'data': {}}
        request = self.factory.post(
            '/webhook/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        response = self.view(request)
        assert response.status_code == 400

    def test_valid_webhook_request(self):
        """Test valid webhook request"""
        mock_transaction_data = {
            'reference': 'test_ref_123',
            'amount': 50000,
            'currency': 'NGN',
            'status': 'success',
            'customer': {
                'email': 'test@example.com',
                'customer_code': 'CUS_xxxxx'
            },
            'authorization': {
                'authorization_code': 'AUTH_xxxxx'
            },
            'channel': 'card',
            'fees': 750,
            'paid_at': '2024-01-15T12:00:00.000Z',
            'metadata': {}
        }

        payload = {
            'event': 'charge.success',
            'data': mock_transaction_data
        }
        payload_bytes = json.dumps(payload).encode('utf-8')

        # Generate valid signature
        secret = 'test_webhook_secret'
        signature = hmac.new(
            secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha512
        ).hexdigest()

        request = self.factory.post(
            '/webhook/',
            data=payload_bytes,
            content_type='application/json',
            HTTP_X_PAYSTACK_SIGNATURE=signature
        )

        with patch('djpaystack.webhooks.views.paystack_settings') as mock_settings:
            mock_settings.WEBHOOK_SECRET = secret
            mock_settings.ENABLE_MODELS = False
            mock_settings.ENABLE_SIGNALS = False

            response = self.view(request)
            assert response.status_code == 200
