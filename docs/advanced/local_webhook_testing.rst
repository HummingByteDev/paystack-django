.. _advanced/local_webhook_testing:

======================
Local Webhook Testing
======================

Testing webhooks locally is essential during development. paystack-django
provides two management commands and a ``WebhookTester`` utility to make
this straightforward.

Overview
========

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Tool
     - Purpose
   * - ``paystack_listen``
     - Start a Cloudflare Tunnel so Paystack can reach your local server
   * - ``paystack_webhook_event``
     - Send a simulated webhook event to your local server
   * - ``WebhookTester`` class
     - Programmatic webhook simulation for automated tests

Step-by-Step Workflow
=====================

1. **Start your Django server:**

   .. code-block:: bash

      python manage.py runserver

2. **In a second terminal, start the tunnel:**

   .. code-block:: bash

      python manage.py paystack_listen

   Copy the printed **Webhook URL** and paste it in
   `Paystack Dashboard → Settings → API Keys & Webhooks <https://dashboard.paystack.com/settings/developer>`_.

3. **In a third terminal, send a test event:**

   .. code-block:: bash

      python manage.py paystack_webhook_event charge.success

   Or trigger a real event from Paystack (e.g. complete a test payment).

``paystack_webhook_event``
==========================

This command sends a properly signed webhook POST request to your local
server. It uses ``PAYSTACK['SECRET_KEY']`` to generate the HMAC signature,
exactly as Paystack does in production.

Basic Usage
-----------

.. code-block:: bash

   # Charge events
   python manage.py paystack_webhook_event charge.success

   # Transfer events
   python manage.py paystack_webhook_event transfer.success --amount 100000

   # Subscription events
   python manage.py paystack_webhook_event subscription.create --email user@example.com

   # Custom data
   python manage.py paystack_webhook_event charge.success \
       --data '{"reference": "my_ref_123", "amount": 75000}'

Options
-------

.. code-block:: text

   event_type              Event type (e.g. charge.success)
   --url URL               Target webhook URL (default: http://localhost:8000/paystack/webhook/)
   --data JSON             Custom JSON payload (overrides sample data)
   --reference REF         Transaction reference (auto-generated if omitted)
   --amount KOBO           Amount in kobo (default: 50000)
   --email EMAIL           Customer email (default: test@example.com)
   --list                  List all supported event types

Listing Available Events
------------------------

.. code-block:: bash

   python manage.py paystack_webhook_event --list

Output:

.. code-block:: text

   Paystack Webhook Event Types

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     Charge:
       ● charge.success
     Transfer:
       ● transfer.success
       ● transfer.failed
       ● transfer.reversed
     Subscription:
       ● subscription.create
       ● subscription.disable
     Refund:
       ● refund.processed
       ● refund.failed
     Dispute:
       ● charge.dispute.create
       ● charge.dispute.resolve
     ...
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ● = sample data included   ○ = use --data for custom payload

``WebhookTester`` (Programmatic)
================================

For automated tests you can use the ``WebhookTester`` class directly:

.. code-block:: python

   from djpaystack.dev.webhook_tester import WebhookTester

   tester = WebhookTester(
       webhook_url='http://localhost:8000/paystack/webhook/',
       secret_key='sk_test_xxxxx',
   )

   # Send any event
   response = tester.send_event('charge.success', {
       'reference': 'test_001',
       'amount': 50000,
       'status': 'success',
       'customer': {'email': 'test@example.com'},
   })
   assert response.status_code == 200

Convenience methods are available for common events:

.. code-block:: python

   tester.send_charge_success(reference='ref_001', amount=50000, email='a@b.com')
   tester.send_subscription_create(email='a@b.com')
   tester.send_transfer_success(amount=100000)

Django TestCase Example
-----------------------

.. code-block:: python

   import json, hashlib, hmac
   from django.test import TestCase, RequestFactory
   from unittest.mock import patch
   from djpaystack.webhooks.handlers import webhook_handler
   from djpaystack.webhooks.views import PaystackWebhookView

   class WebhookIntegrationTest(TestCase):
       def test_charge_success_webhook(self):
           secret = 'sk_test_xxxxx'
           payload = json.dumps({
               'event': 'charge.success',
               'data': {
                   'reference': 'test_ref',
                   'amount': 50000,
                   'status': 'success',
                   'customer': {'email': 'test@example.com'},
               },
           }).encode()

           signature = hmac.new(
               secret.encode(), payload, hashlib.sha512
           ).hexdigest()

           factory = RequestFactory()
           request = factory.post(
               '/webhook/',
               data=payload,
               content_type='application/json',
               HTTP_X_PAYSTACK_SIGNATURE=signature,
           )

           with patch('djpaystack.webhooks.handlers.paystack_settings') as mock:
               mock.SECRET_KEY = secret
               mock.ENABLE_MODELS = False
               mock.ENABLE_SIGNALS = False
               with patch.object(webhook_handler, 'verify_ip', return_value=True):
                   response = PaystackWebhookView.as_view()(request)
                   self.assertEqual(response.status_code, 200)

Troubleshooting
===============

**"SECRET_KEY not configured"**
   Make sure ``PAYSTACK['SECRET_KEY']`` is set in your Django settings.

**Webhook returns 403 — Unauthorized IP**
   During local testing, the request comes from ``127.0.0.1``, which isn't
   in Paystack's IP whitelist. Either:

   - Clear ``ALLOWED_WEBHOOK_IPS`` in settings (allows all IPs), or
   - Add ``127.0.0.1`` to the whitelist during development.

**Webhook returns 400 — Invalid signature**
   The ``SECRET_KEY`` used to send the test event must match the one
   configured in your Django settings.

**Connection refused**
   Make sure ``python manage.py runserver`` is running on the expected port.
