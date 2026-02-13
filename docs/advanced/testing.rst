.. _advanced/testing:

Testing
=======

Test your Paystack integration thoroughly.

Unit Testing
------------

Test individual API methods:

.. code-block:: python

    from django.test import TestCase
    from unittest.mock import patch, MagicMock
    from djpaystack.api.transactions import Transaction

    class TransactionTestCase(TestCase):
        
        def setUp(self):
            self.transaction = Transaction()
        
        @patch('djpaystack.api.transactions.requests.post')
        def test_initialize_transaction(self, mock_post):
            # Mock API response
            mock_post.return_value.json.return_value = {
                'status': True,
                'message': 'Authorization URL created',
                'data': {
                    'authorization_url': 'https://checkout.paystack.com/...',
                    'access_code': 'ACCESS_CODE',
                    'reference': 'UNIQUE_REF',
                }
            }
            
            response = self.transaction.initialize(
                email='test@example.com',
                amount=50000
            )
            
            self.assertTrue(response['status'])
            self.assertIn('authorization_url', response['data'])

        @patch('djpaystack.api.transactions.requests.get')
        def test_verify_transaction(self, mock_get):
            # Mock API response
            mock_get.return_value.json.return_value = {
                'status': True,
                'data': {
                    'reference': 'UNIQUE_REF',
                    'amount': 50000,
                    'status': 'success',
                }
            }
            
            response = self.transaction.verify('UNIQUE_REF')
            
            self.assertTrue(response['status'])
            self.assertEqual(response['data']['status'], 'success')

Integration Testing
-------------------

Test with real API (use test credentials):

.. code-block:: python

    from django.test import TestCase, override_settings
    from djpaystack.api.transactions import Transaction

    @override_settings(PAYSTACK={
        'SECRET_KEY': 'sk_test_...',
        'PUBLIC_KEY': 'pk_test_...',
    })
    class IntegrationTestCase(TestCase):
        
        def test_payment_flow(self):
            """Test complete payment flow"""
            transaction = Transaction()
            
            # Initialize
            init_response = transaction.initialize(
                email='test@example.com',
                amount=50000
            )
            self.assertTrue(init_response['status'])
            
            reference = init_response['data']['reference']
            
            # Note: In real testing, user would complete payment
            # Then verify
            verify_response = transaction.verify(reference)
            # Results depends on whether payment was completed

View Testing
------------

Test your payment views:

.. code-block:: python

    from django.test import TestCase, Client
    from unittest.mock import patch

    class PaymentViewTestCase(TestCase):
        
        def setUp(self):
            self.client = Client()
        
        @patch('myapp.views.Transaction.initialize')
        def test_checkout_view(self, mock_initialize):
            mock_initialize.return_value = {
                'status': True,
                'data': {
                    'authorization_url': 'https://checkout.paystack.com/...',
                    'reference': 'TEST_REF',
                }
            }
            
            response = self.client.post('/checkout/', {
                'email': 'test@example.com',
                'amount': '500',
            })
            
            self.assertEqual(response.status_code, 302)  # Redirect

Webhook Testing
---------------

Test webhook handling:

.. code-block:: python

    from django.test import TestCase, Client
    from django.urls import reverse
    import json
    from unittest.mock import patch

    class WebhookTestCase(TestCase):
        
        def setUp(self):
            self.client = Client()
            self.webhook_url = reverse('paystack-webhook')
        
        @patch('djpaystack.webhooks.handlers.verify_webhook_signature')
        def test_charge_success_webhook(self, mock_verify):
            mock_verify.return_value = True
            
            payload = {
                'event': 'charge.success',
                'data': {
                    'reference': 'TEST_REF',
                    'amount': 50000,
                    'customer': {'email': 'test@example.com'},
                    'status': 'success',
                }
            }
            
            response = self.client.post(
                self.webhook_url,
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)

Testing Utilities
-----------------

Use the built-in test utilities:

.. code-block:: python

    from djpaystack.dev.webhook_tester import WebhookTester
    from djpaystack.dev.mock_client import MockPaystackClient

    # Test webhooks
    tester = WebhookTester()
    tester.test_charge_success({
        'reference': 'test-123',
        'amount': 50000,
    })

    # Mock client for testing
    mock_client = MockPaystackClient()
    response = mock_client.initialize(
        email='test@example.com',
        amount=50000
    )

Best Practices
--------------

1. Use test credentials, never live keys
2. Mock external API calls
3. Test both success and failure cases
4. Test error handling
5. Use factories for test data
6. Keep tests isolated
7. Test at multiple levels (unit, integration, end-to-end)

.. code-block:: python

    import factory
    from djpaystack.models import Transaction

    class TransactionFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = Transaction
        
        reference = factory.Sequence(lambda n: f'TEST_REF_{n}')
        amount = 50000
        customer_email = 'test@example.com'
        status = 'pending'
