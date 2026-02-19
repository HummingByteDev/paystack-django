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

2. **Set the Webhook Secret:**

   In the `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_,
   add your URL and copy the secret:

   .. code-block:: python

       PAYSTACK = {
           'SECRET_KEY': 'sk_...',
           'PUBLIC_KEY': 'pk_...',
           'WEBHOOK_SECRET': 'whsec_...',
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
   * - ``charge.failed``
     - Payment attempt failed
   * - ``charge.dispute.create``
     - New dispute opened
   * - ``charge.dispute.remind``
     - Dispute reminder
   * - ``charge.dispute.resolve``
     - Dispute resolved
   * - ``transfer.success``
     - Transfer completed
   * - ``transfer.failed``
     - Transfer failed
   * - ``transfer.reversed``
     - Transfer reversed
   * - ``bank.transfer.rejected``
     - Bank transfer rejected
   * - ``subscription.create``
     - Subscription created
   * - ``subscription.disable``
     - Subscription disabled
   * - ``subscription.not_renew``
     - Subscription will not renew
   * - ``refund.pending``
     - Refund initiated
   * - ``refund.processing``
     - Refund being processed
   * - ``refund.processed``
     - Refund completed
   * - ``refund.failed``
     - Refund failed
   * - ``refund.needs-attention``
     - Refund requires manual intervention
   * - ``dedicatedaccount.assign.success``
     - DVA assigned successfully
   * - ``direct_debit.authorization.created``
     - Direct debit authorization created
   * - ``direct_debit.authorization.active``
     - Direct debit authorization activated

See ``djpaystack.webhooks.events.WebhookEvent`` for the full enum.

Custom Handlers
---------------

Register a custom handler that overrides or extends the default behaviour:

.. code-block:: python

    from djpaystack.webhooks.handlers import WebhookHandler
    from djpaystack.webhooks.events import WebhookEvent

    handler = WebhookHandler()

    @handler.register(WebhookEvent.CHARGE_SUCCESS)
    def my_charge_success(data):
        reference = data['reference']
        # Your custom logic here

Django Signals
--------------

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import (
        paystack_payment_successful,
        paystack_payment_failed,
        paystack_transfer_successful,
        paystack_refund_processed,
        paystack_dispute_created,
    )

    @receiver(paystack_payment_successful)
    def on_payment(sender, transaction_data, **kwargs):
        print(f"Paid: {transaction_data['reference']}")

Testing Webhooks Locally
------------------------

Use `ngrok <https://ngrok.com>`_ to expose your local server:

.. code-block:: bash

    ngrok http 8000
    # Use https://xxxx.ngrok.io/webhooks/paystack/ as your webhook URL

Best Practices
--------------

1. **Always configure WEBHOOK_SECRET** — Without it, all requests are rejected.
2. **Respond quickly** — Return ``200`` within 5 seconds. Offload heavy work to Celery.
3. **Process idempotently** — The same event may be delivered more than once.
4. **Log events** — ``PaystackWebhookEvent`` model stores all received events.
5. **Monitor failures** — Check ``PaystackWebhookEvent.objects.filter(processed=False)``.

For advanced patterns, see :ref:`advanced/webhooks`.
