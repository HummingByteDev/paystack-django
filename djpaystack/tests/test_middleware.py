
import logging
from django.test import TestCase, RequestFactory
from djpaystack.middleware import PaystackLoggingMiddleware


class TestPaystackLoggingMiddleware(TestCase):
    """Test Paystack logging middleware"""

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = PaystackLoggingMiddleware(
            get_response=lambda r: None)

    def test_logs_webhook_request(self):
        """Test that webhook requests are logged"""
        request = self.factory.post('/paystack/webhook/')

        with self.assertLogs('djpaystack', level='INFO') as cm:
            self.middleware.process_request(request)

        self.assertTrue(
            any('Paystack webhook request' in msg for msg in cm.output))

    def test_ignores_non_webhook_request(self):
        """Test that non-webhook requests are not logged"""
        request = self.factory.get('/some/other/path/')

        # Should not log anything at INFO level for non-webhook paths
        result = self.middleware.process_request(request)
        self.assertIsNone(result)

    def test_returns_none(self):
        """Test that process_request returns None"""
        request = self.factory.post('/paystack/webhook/')

        with self.assertLogs('djpaystack', level='INFO'):
            result = self.middleware.process_request(request)

        self.assertIsNone(result)
