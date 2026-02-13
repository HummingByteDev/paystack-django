
import json
import hmac
import hashlib
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import logging
from ..webhooks.events import WebhookEvent


logger = logging.getLogger('djpaystack.dev')


class WebhookTester:
    """
    Test webhook events locally
    Simulates Paystack webhook events for development
    """

    def __init__(self, webhook_url: str, webhook_secret: str):
        """
        Initialize webhook tester

        Args:
            webhook_url: Local webhook URL (e.g., http://localhost:8000/paystack/webhook/)
            webhook_secret: Webhook secret for signature generation
        """
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret

    def _generate_signature(self, payload: bytes) -> str:
        """Generate webhook signature"""
        return hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()

    def send_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send webhook event to local server

        Args:
            event_type: Event type (e.g., 'charge.success')
            data: Event data
            headers: Additional headers

        Returns:
            Response from webhook endpoint
        """
        payload = {
            'event': event_type,
            'data': data
        }

        payload_bytes = json.dumps(payload).encode('utf-8')
        signature = self._generate_signature(payload_bytes)

        request_headers = {
            'Content-Type': 'application/json',
            'X-Paystack-Signature': signature,
        }

        if headers:
            request_headers.update(headers)

        logger.info(f"Sending test webhook: {event_type}")

        response = requests.post(
            self.webhook_url,
            data=payload_bytes,
            headers=request_headers
        )

        logger.info(f"Webhook response: {response.status_code}")
        return response

    # Convenience methods for common events

    def send_charge_success(
        self,
        reference: str = 'test_ref_123',
        amount: int = 50000,
        email: str = 'test@example.com',
        **kwargs
    ) -> requests.Response:
        """Send successful charge event"""
        data = {
            'reference': reference,
            'amount': amount,
            'currency': 'NGN',
            'status': 'success',
            'paid_at': datetime.now().isoformat(),
            'customer': {
                'email': email,
                'customer_code': 'CUS_test123'
            },
            'authorization': {
                'authorization_code': 'AUTH_test123',
                'bin': '539983',
                'last4': '1234',
                'exp_month': '12',
                'exp_year': '2025',
                'card_type': 'visa',
                'bank': 'Test Bank'
            },
            'channel': 'card',
            'fees': 750,
            'metadata': kwargs.get('metadata', {})
        }

        return self.send_event(WebhookEvent.CHARGE_SUCCESS, data)

    def send_charge_failed(
        self,
        reference: str = 'test_ref_456',
        amount: int = 50000,
        email: str = 'test@example.com'
    ) -> requests.Response:
        """Send failed charge event"""
        data = {
            'reference': reference,
            'amount': amount,
            'currency': 'NGN',
            'status': 'failed',
            'customer': {
                'email': email,
                'customer_code': 'CUS_test123'
            },
            'gateway_response': 'Insufficient funds',
            'metadata': {}
        }

        return self.send_event(WebhookEvent.CHARGE_FAILED, data)

    def send_subscription_create(
        self,
        subscription_code: str = 'SUB_test123',
        email: str = 'test@example.com'
    ) -> requests.Response:
        """Send subscription creation event"""
        data = {
            'subscription_code': subscription_code,
            'email_token': 'token_123',
            'amount': 100000,
            'status': 'active',
            'customer': {
                'email': email,
                'customer_code': 'CUS_test123'
            },
            'plan': {
                'plan_code': 'PLN_test123',
                'name': 'Premium Plan',
                'interval': 'monthly'
            },
            'authorization': {
                'authorization_code': 'AUTH_test123'
            },
            'next_payment_date': datetime.now().isoformat()
        }

        return self.send_event(WebhookEvent.SUBSCRIPTION_CREATE, data)

    def send_transfer_success(
        self,
        transfer_code: str = 'TRF_test123',
        amount: int = 100000
    ) -> requests.Response:
        """Send successful transfer event"""
        data = {
            'transfer_code': transfer_code,
            'reference': f'ref_{transfer_code}',
            'amount': amount,
            'currency': 'NGN',
            'status': 'success',
            'transferred_at': datetime.now().isoformat(),
            'recipient': {
                'recipient_code': 'RCP_test123',
                'name': 'John Doe',
                'type': 'nuban',
                'account_number': '0123456789',
                'bank_code': '058'
            },
            'reason': 'Test transfer'
        }

        return self.send_event(WebhookEvent.TRANSFER_SUCCESS, data)


def send_test_webhook(
    event_type: str,
    data: Dict[str, Any],
    webhook_url: str = 'http://localhost:8000/paystack/webhook/',
    webhook_secret: str = 'test_webhook_secret'
) -> requests.Response:
    """
    Convenience function to send test webhook

    Args:
        event_type: Webhook event type
        data: Event data
        webhook_url: Local webhook URL
        webhook_secret: Webhook secret

    Returns:
        Response from webhook endpoint
    """
    tester = WebhookTester(webhook_url, webhook_secret)
    return tester.send_event(event_type, data)
