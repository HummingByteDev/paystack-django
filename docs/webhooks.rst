.. _webhooks:

Webhooks
========

paystack-django includes a production-ready webhook system with signature verification,
IP whitelisting, event deduplication, Django model persistence, and Django signal dispatch.

Setup
-----

1. **Add the URL endpoint:**

   .. code-block:: python

       # urls.py
       from django.urls import path
       from djpaystack.webhooks.views import handle_webhook

       urlpatterns = [
           path('webhooks/paystack/', handle_webhook, name='paystack-webhook'),
       ]

2. **Configure your secret key:**

   Paystack uses your API secret key to sign webhooks.
   In the `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_,
   add your webhook URL. No separate webhook secret is needed:

   .. code-block:: python

       PAYSTACK = {
           'SECRET_KEY': 'sk_...',
           'PUBLIC_KEY': 'pk_...',
       }

How It Works
------------

When Paystack sends a webhook:

1. **Signature verified** — HMAC SHA-512 of the raw body is compared against ``X-Paystack-Signature``.
2. **IP checked** — Request IP is compared against Paystack's known IPs (or your custom whitelist).
3. **Event deduplicated** — Duplicate events (same reference + event type) are skipped.
4. **Handler dispatched** — The registered handler for the event type is called.
5. **Model saved** — If ``ENABLE_MODELS`` is ``True``, data is persisted to ``PaystackWebhookEvent``.
6. **Signal sent** — If ``ENABLE_SIGNALS`` is ``True``, the appropriate Django signal fires.

Supported Webhook Events
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Event
     - Description
   * - ``charge.success``
     - Payment completed successfully
   * - ``charge.dispute.create``
     - New dispute opened
   * - ``charge.dispute.remind``
     - Dispute reminder sent
   * - ``charge.dispute.resolve``
     - Dispute resolved
   * - ``customeridentification.success``
     - Customer identity verification succeeded
   * - ``customeridentification.failed``
     - Customer identity verification failed
   * - ``dedicatedaccount.assign.success``
     - Dedicated Virtual Account assigned
   * - ``dedicatedaccount.assign.failed``
     - Dedicated Virtual Account assignment failed
   * - ``invoice.create``
     - New invoice created
   * - ``invoice.update``
     - Invoice updated
   * - ``invoice.payment_failed``
     - Invoice payment failed
   * - ``paymentrequest.pending``
     - Payment request pending
   * - ``paymentrequest.success``
     - Payment request paid
   * - ``refund.pending``
     - Refund initiated
   * - ``refund.processing``
     - Refund being processed
   * - ``refund.processed``
     - Refund completed
   * - ``refund.failed``
     - Refund failed
   * - ``subscription.create``
     - Subscription created
   * - ``subscription.disable``
     - Subscription disabled / cancelled
   * - ``subscription.not_renew``
     - Subscription will not renew
   * - ``subscription.expiring_cards``
     - Cards on subscriptions are about to expire
   * - ``transfer.success``
     - Transfer completed
   * - ``transfer.failed``
     - Transfer failed
   * - ``transfer.reversed``
     - Transfer reversed

See ``djpaystack.webhooks.events.WebhookEvent`` for the full enum.

Custom Handlers
---------------

Register a custom handler that overrides or extends the default behaviour:

.. code-block:: python

    from djpaystack.webhooks.handlers import webhook_handler
    from djpaystack.webhooks.events import WebhookEvent

    def my_charge_success(data):
        reference = data['reference']
        # Your custom logic here

    # Override the default handler
    webhook_handler.register(WebhookEvent.CHARGE_SUCCESS, my_charge_success)

Django Signals
--------------

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import (
        paystack_payment_successful,
        paystack_transfer_successful,
        paystack_refund_processed,
        paystack_dispute_created,
        paystack_invoice_created,
        paystack_customeridentification_success,
    )

    @receiver(paystack_payment_successful)
    def on_payment(sender, transaction_data, **kwargs):
        print(f"Paid: {transaction_data['reference']}")

Testing Webhooks Locally
------------------------

Use the built-in ``paystack_listen`` command to expose your local server
via a Cloudflare Tunnel:

.. code-block:: bash

    python manage.py paystack_listen
    # Displays https://xxxx.trycloudflare.com/paystack/webhook/

Or send simulated events directly:

.. code-block:: bash

    python manage.py paystack_webhook_event charge.success

See :ref:`advanced/cloudflare_tunnel` and :ref:`advanced/local_webhook_testing`
for full documentation.

Best Practices
--------------

1. **Keep your SECRET_KEY safe** — Webhook signatures are verified using your API secret key.
2. **Respond quickly** — Return ``200`` within 5 seconds. Offload heavy work to Celery.
3. **Process idempotently** — The same event may be delivered more than once.
4. **Log events** — ``PaystackWebhookEvent`` model stores all received events.
5. **Monitor failures** — Check ``PaystackWebhookEvent.objects.filter(processed=False)``.

For advanced patterns, see :ref:`advanced/webhooks` and :ref:`advanced/webhook_security`.
