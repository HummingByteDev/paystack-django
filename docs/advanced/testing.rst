.. _advanced/testing:

=======
Testing
=======

Strategies for testing your Paystack integration.

Unit Testing API Calls
======================

Mock the HTTP layer so tests never hit the real Paystack API:

.. code-block:: python

    from django.test import TestCase
    from unittest.mock import patch, MagicMock
    from djpaystack import PaystackClient

    class TransactionTestCase(TestCase):

        def setUp(self):
            self.client = PaystackClient()

        @patch('djpaystack.api.base.requests.Session.request')
        def test_initialize_transaction(self, mock_request):
            mock_request.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    'status': True,
                    'message': 'Authorization URL created',
                    'data': {
                        'authorization_url': 'https://checkout.paystack.com/...',
                        'access_code': 'ACCESS_CODE',
                        'reference': 'UNIQUE_REF',
                    },
                },
            )

            response = self.client.transactions.initialize(
                email='test@example.com',
                amount=50000,
            )
            self.assertTrue(response['status'])
            self.assertIn('authorization_url', response['data'])

        @patch('djpaystack.api.base.requests.Session.request')
        def test_verify_transaction(self, mock_request):
            mock_request.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    'status': True,
                    'data': {
                        'reference': 'UNIQUE_REF',
                        'amount': 50000,
                        'status': 'success',
                    },
                },
            )

            response = self.client.transactions.verify('UNIQUE_REF')
            self.assertTrue(response['status'])
            self.assertEqual(response['data']['status'], 'success')

Integration Testing
===================

Use **test** credentials (``sk_test_...``) to hit the real API in a CI
environment:

.. code-block:: python

    from django.test import TestCase, override_settings
    from djpaystack import PaystackClient

    @override_settings(PAYSTACK={
        'SECRET_KEY': 'sk_test_...',
        'PUBLIC_KEY': 'pk_test_...',
    })
    class IntegrationTestCase(TestCase):

        def test_payment_flow(self):
            client = PaystackClient()
            init = client.transactions.initialize(
                email='test@example.com', amount=50000,
            )
            self.assertTrue(init['status'])

View Testing
============

.. code-block:: python

    from django.test import TestCase, Client
    from unittest.mock import patch

    class PaymentViewTestCase(TestCase):

        def setUp(self):
            self.http = Client()

        @patch('myapp.views.PaystackClient')
        def test_checkout_view(self, MockClient):
            MockClient.return_value.transactions.initialize.return_value = {
                'status': True,
                'data': {
                    'authorization_url': 'https://checkout.paystack.com/...',
                    'reference': 'TEST_REF',
                },
            }
            response = self.http.post('/checkout/', {
                'email': 'test@example.com',
                'amount': '500',
            })
            self.assertEqual(response.status_code, 302)

Webhook Testing
===============

Generate a correctly signed request from the test suite:

.. code-block:: python

    import hmac, hashlib, json
    from django.test import TestCase, Client, override_settings
    from django.urls import reverse

    SECRET = 'sk_test_xxx'

    @override_settings(PAYSTACK={'SECRET_KEY': SECRET})
    class WebhookTestCase(TestCase):

        def _signed_post(self, payload_dict):
            body = json.dumps(payload_dict)
            sig = hmac.new(
                SECRET.encode(), body.encode(), hashlib.sha512,
            ).hexdigest()
            return self.client.post(
                reverse('paystack-webhook'),
                data=body,
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE=sig,
            )

        def test_charge_success(self):
            resp = self._signed_post({
                'event': 'charge.success',
                'data': {
                    'reference': 'TEST_REF',
                    'amount': 50000,
                    'customer': {'email': 'test@example.com'},
                    'status': 'success',
                },
            })
            self.assertEqual(resp.status_code, 200)

        def test_invalid_signature_rejected(self):
            resp = self.client.post(
                reverse('paystack-webhook'),
                data='{}',
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE='bad',
            )
            self.assertEqual(resp.status_code, 401)

Using ``paystack_webhook_event``
================================

Fire a simulated webhook at your running dev server from the command line:

.. code-block:: bash

    # Send a charge.success event with default sample data
    python manage.py paystack_webhook_event charge.success

    # Custom reference and amount
    python manage.py paystack_webhook_event charge.success \
        --reference order_123 --amount 75000

    # Completely custom payload
    python manage.py paystack_webhook_event charge.success \
        --data '{"reference": "custom", "amount": 50000}'

See :ref:`advanced/local_webhook_testing` for the full workflow.

Testing Utilities
=================

``WebhookTester`` (in ``djpaystack.dev.webhook_tester``) sends signed
webhook requests programmatically:

.. code-block:: python

    from djpaystack.dev.webhook_tester import WebhookTester

    tester = WebhookTester(
        base_url='http://localhost:8000',
        secret_key='sk_test_xxx',
    )
    response = tester.send_test_webhook(
        event='charge.success',
        data={'reference': 'test-123', 'amount': 50000},
    )
    assert response.status_code == 200

Best Practices
==============

1. **Use test credentials** — never live keys in CI or local dev.
2. **Mock external calls** — patch ``requests.Session.request`` to keep tests fast and deterministic.
3. **Test success and failure paths** — verify both happy-path and error responses.
4. **Keep tests isolated** — use ``override_settings`` so each test has its own config.
5. **Test signal handlers** — send signals manually and assert side-effects.
6. **Run the full suite before pushing** — ``python -m pytest djpaystack/tests/ -v``.
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
