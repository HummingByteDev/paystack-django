.. _webhooks:

Webhooks
========

Handle real-time payment notifications with webhooks.

Setting Up Webhooks
-------------------

1. **Add to Django URLs:**

   .. code-block:: python

       # urls.py
       from django.urls import path
       from djpaystack.webhooks.views import webhook

       urlpatterns = [
           path('api/webhooks/paystack/', webhook, name='paystack-webhook'),
       ]

2. **Configure Paystack Dashboard:**

   - Go to Settings > API Keys & Webhooks
   - Add your webhook URL: ``https://yourdomain.com/api/webhooks/paystack/``
   - Copy the webhook secret

3. **Add to Django Settings:**

   .. code-block:: python

       PAYSTACK = {
           'SECRET_KEY': 'sk_...',
           'PUBLIC_KEY': 'pk_...',
           'WEBHOOK_SECRET': 'whsec_...',  # From dashboard
       }

Webhook Events
--------------

Common webhook events:

- ``charge.success`` - Payment successful
- ``charge.failed`` - Payment failed
- ``subscription.create`` - Subscription created
- ``subscription.disable`` - Subscription disabled
- ``transfer.success`` - Transfer successful
- ``transfer.failed`` - Transfer failed

Creating Custom Handlers
------------------------

Create a handler for webhook events:

.. code-block:: python

    # webhooks.py
    from djpaystack.webhooks.handlers import BaseWebhookHandler
    from djpaystack.models import Transaction

    class CustomWebhookHandler(BaseWebhookHandler):
        
        def handle_charge_success(self, data):
            """Handle successful payment"""
            reference = data['reference']
            
            # Update your records
            Transaction.objects.filter(
                reference=reference
            ).update(status='success', paid_at=timezone.now())
        
        def handle_charge_failed(self, data):
            """Handle failed payment"""
            reference = data['reference']
            
            # Update your records
            Transaction.objects.filter(
                reference=reference
            ).update(status='failed')

Testing Webhooks
----------------

Test webhooks locally with ngrok:

.. code-block:: bash

    # Start ngrok
    ngrok http 8000

    # Use the provided URL as your webhook endpoint
    # https://xxxxxx.ngrok.io/api/webhooks/paystack/

Or use the built-in webhook tester:

.. code-block:: python

    from djpaystack.dev.webhook_tester import WebhookTester

    tester = WebhookTester()
    tester.test_charge_success({
        'reference': 'test-123',
        'amount': 50000,
        'email': 'test@example.com'
    })

Best Practices
--------------

1. Always verify webhook signatures
2. Respond quickly (within 3 seconds)
3. Process webhooks idempotently
4. Log all webhook events
5. Use async processing for heavy operations

For more details, see :ref:`advanced/webhooks`.
