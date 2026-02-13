from django.test import TestCase
from djpaystack.models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackWebhookEvent,
)


class TestPaystackModels(TestCase):
    """Test Paystack models"""

    def test_create_transaction(self):
        """Test creating transaction"""
        transaction = PaystackTransaction.objects.create(
            reference='test_ref_123',
            amount=50000,
            currency='NGN',
            status='success',
            customer_email='test@example.com'
        )

        assert transaction.reference == 'test_ref_123'
        assert transaction.amount == 50000
        assert str(transaction) == 'test_ref_123 - success'

    def test_create_customer(self):
        """Test creating customer"""
        customer = PaystackCustomer.objects.create(
            customer_code='CUS_xxxxx',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

        assert customer.customer_code == 'CUS_xxxxx'
        assert customer.email == 'test@example.com'
        assert str(customer) == 'test@example.com (CUS_xxxxx)'

    def test_create_webhook_event(self):
        """Test creating webhook event"""
        event = PaystackWebhookEvent.objects.create(
            event_type='charge.success',
            event_id='evt_123',
            data={'reference': 'test_ref'}
        )

        assert event.event_type == 'charge.success'
        assert event.processed is False
        assert str(event) == 'charge.success - evt_123'
