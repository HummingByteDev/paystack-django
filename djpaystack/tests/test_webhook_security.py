
from unittest.mock import patch

from django.test import TestCase

from djpaystack.webhooks.handlers import webhook_handler, PAYSTACK_WEBHOOK_IPS


class TestWebhookIPVerification(TestCase):
    """Test webhook IP verification"""

    def test_paystack_ip_allowed(self):
        """Test that Paystack IPs are allowed by default"""
        for ip in PAYSTACK_WEBHOOK_IPS:
            with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
                mock_settings.ALLOWED_WEBHOOK_IPS = []
                result = webhook_handler.verify_ip(ip)
                self.assertTrue(result, f"Paystack IP {ip} should be allowed")

    def test_unknown_ip_rejected(self):
        """Test that unknown IPs are rejected"""
        with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
            mock_settings.ALLOWED_WEBHOOK_IPS = []
            result = webhook_handler.verify_ip('192.168.1.100')
            self.assertFalse(result)

    def test_custom_whitelist(self):
        """Test custom IP whitelist"""
        with patch('djpaystack.webhooks.handlers.paystack_settings') as mock_settings:
            mock_settings.ALLOWED_WEBHOOK_IPS = ['10.0.0.1', '10.0.0.2']
            self.assertTrue(webhook_handler.verify_ip('10.0.0.1'))
            self.assertFalse(webhook_handler.verify_ip('10.0.0.3'))


class TestWebhookDeduplication(TestCase):
    """Test webhook event deduplication with OrderedDict"""

    def test_mark_and_detect_duplicate(self):
        """Test basic mark and detect flow"""
        handler = webhook_handler

        event_id = 'dedup_test_1'
        handler._processed_events.pop(event_id, None)  # Clean up

        self.assertFalse(handler.is_duplicate_event(event_id))
        handler.mark_event_processed(event_id)
        self.assertTrue(event_id in handler._processed_events)

    def test_eviction_preserves_recent_entries(self):
        """Test that OrderedDict eviction keeps newest entries"""
        from collections import OrderedDict
        handler = webhook_handler

        # Save original and replace with small dict for testing
        original = handler._processed_events
        handler._processed_events = OrderedDict()

        try:
            # Add 1001 entries to trigger eviction (limit is 1000)
            for i in range(1001):
                handler.mark_event_processed(f"evt_{i}")

            # Should have exactly 1000 entries
            self.assertEqual(len(handler._processed_events), 1000)

            # First entry should have been evicted
            self.assertNotIn('evt_0', handler._processed_events)

            # Last entry should still be there
            self.assertIn('evt_1000', handler._processed_events)
        finally:
            handler._processed_events = original
