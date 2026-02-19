.. _quickstart:

Quick Start
===========

Get up and running with paystack-django in 5 minutes.

1. Install
----------

.. code-block:: bash

    pip install paystack-django

2. Django Settings
------------------

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        # ...
        'djpaystack',
    ]

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_your_secret_key_here',
        'PUBLIC_KEY': 'pk_test_your_public_key_here',
        'WEBHOOK_SECRET': 'whsec_your_webhook_secret',
    }

3. Run Migrations
-----------------

.. code-block:: bash

    python manage.py migrate djpaystack

4. Initialize a Transaction
----------------------------

.. code-block:: python

    from djpaystack import PaystackClient

    client = PaystackClient()

    response = client.transactions.initialize(
        email='customer@example.com',
        amount=50000,  # 500 NGN in kobo
    )

    authorization_url = response['data']['authorization_url']
    # Redirect the user to authorization_url

Or use the client as a context manager:

.. code-block:: python

    with PaystackClient() as client:
        response = client.transactions.initialize(
            email='customer@example.com',
            amount=50000,
        )

5. Verify Payment
-----------------

After the user completes payment on Paystack's hosted page:

.. code-block:: python

    response = client.transactions.verify(reference='ref-from-step-4')

    if response['data']['status'] == 'success':
        # Payment confirmed — fulfil the order
        print(f"Paid: {response['data']['amount']} kobo")

6. Handle Webhooks
------------------

Add the webhook endpoint to your ``urls.py``:

.. code-block:: python

    from django.urls import path
    from djpaystack.webhooks.views import handle_webhook

    urlpatterns = [
        path('webhooks/paystack/', handle_webhook, name='paystack-webhook'),
    ]

Then add your webhook URL (``https://yourdomain.com/webhooks/paystack/``) in the
`Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_.

7. Listen for Signals
---------------------

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_payment_successful

    @receiver(paystack_payment_successful)
    def on_payment(sender, transaction_data, **kwargs):
        ref = transaction_data['reference']
        # Update your order, send receipt, etc.

Complete Example View
---------------------

.. code-block:: python

    import uuid
    from django.shortcuts import redirect
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from djpaystack import PaystackClient

    @require_http_methods(["POST"])
    def checkout(request):
        client = PaystackClient()
        response = client.transactions.initialize(
            email=request.POST['email'],
            amount=int(request.POST['amount']),
            reference=f"order-{uuid.uuid4().hex[:12]}",
            metadata={'user_id': request.user.id},
        )
        return redirect(response['data']['authorization_url'])

    @require_http_methods(["GET"])
    def callback(request):
        ref = request.GET.get('reference')
        client = PaystackClient()
        result = client.transactions.verify(reference=ref)
        if result['data']['status'] == 'success':
            return JsonResponse({'message': 'Payment successful', 'reference': ref})
        return JsonResponse({'message': 'Payment failed'}, status=400)

Tips
----

1. **Always use HTTPS in production** — Paystack requires secure connections.
2. **Verify server-side** — Never trust client-side verification alone.
3. **Handle webhooks** — Webhooks are more reliable than redirect callbacks.
4. **Use test keys** during development, switch to live keys in production.

What's Next?
------------

- :ref:`configuration` — Full configuration reference
- :ref:`transactions` — Detailed transaction guide
- :ref:`webhooks` — Advanced webhook patterns
- :ref:`api/index` — Complete API reference for all 26 modules
