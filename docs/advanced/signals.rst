.. _advanced/signals:

==============
Django Signals
==============

paystack-django dispatches Django signals when webhook events are processed,
allowing you to hook into the payment lifecycle without modifying library code.

Available Signals
=================

All signals are defined in ``djpaystack.signals``:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Signal
     - Triggered when
   * - ``paystack_payment_successful``
     - ``charge.success`` webhook received
   * - ``paystack_subscription_created``
     - ``subscription.create`` webhook received
   * - ``paystack_subscription_cancelled``
     - ``subscription.disable`` webhook received
   * - ``paystack_subscription_not_renewing``
     - ``subscription.not_renew`` webhook received
   * - ``paystack_subscription_expiring_cards``
     - ``subscription.expiring_cards`` webhook received
   * - ``paystack_transfer_successful``
     - ``transfer.success`` webhook received
   * - ``paystack_transfer_failed``
     - ``transfer.failed`` webhook received
   * - ``paystack_transfer_reversed``
     - ``transfer.reversed`` webhook received
   * - ``paystack_refund_pending``
     - ``refund.pending`` webhook received
   * - ``paystack_refund_processing``
     - ``refund.processing`` webhook received
   * - ``paystack_refund_processed``
     - ``refund.processed`` webhook received
   * - ``paystack_refund_failed``
     - ``refund.failed`` webhook received
   * - ``paystack_dispute_created``
     - ``charge.dispute.create`` webhook received
   * - ``paystack_dispute_remind``
     - ``charge.dispute.remind`` webhook received
   * - ``paystack_dispute_resolved``
     - ``charge.dispute.resolve`` webhook received
   * - ``paystack_customeridentification_success``
     - ``customeridentification.success`` webhook received
   * - ``paystack_customeridentification_failed``
     - ``customeridentification.failed`` webhook received
   * - ``paystack_dedicatedaccount_assign_success``
     - ``dedicatedaccount.assign.success`` webhook received
   * - ``paystack_dedicatedaccount_assign_failed``
     - ``dedicatedaccount.assign.failed`` webhook received
   * - ``paystack_invoice_created``
     - ``invoice.create`` webhook received
   * - ``paystack_invoice_updated``
     - ``invoice.update`` webhook received
   * - ``paystack_invoice_payment_failed``
     - ``invoice.payment_failed`` webhook received
   * - ``paystack_paymentrequest_pending``
     - ``paymentrequest.pending`` webhook received
   * - ``paystack_paymentrequest_success``
     - ``paymentrequest.success`` webhook received

Connecting to Signals
=====================

Use Django's ``@receiver`` decorator:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import (
        paystack_payment_successful,
    )

    @receiver(paystack_payment_successful)
    def on_payment_success(sender, transaction_data, **kwargs):
        """Called when a charge.success webhook is processed."""
        reference = transaction_data['reference']
        amount = transaction_data['amount']  # in kobo
        # Fulfil the order, send receipt, etc.

Best Practice: Register in ``apps.py``
--------------------------------------

Create a ``signals.py`` module in your app and import it from ``ready()``:

.. code-block:: python

    # myapp/apps.py
    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'myapp'

        def ready(self):
            import myapp.signals  # noqa: F401

.. code-block:: python

    # myapp/signals.py
    from django.dispatch import receiver
    from django.utils import timezone
    from djpaystack.signals import paystack_payment_successful
    from .models import Order

    @receiver(paystack_payment_successful)
    def fulfil_order(sender, transaction_data, **kwargs):
        try:
            order = Order.objects.get(reference=transaction_data['reference'])
            order.status = 'paid'
            order.paid_at = timezone.now()
            order.save()
        except Order.DoesNotExist:
            pass  # Log or handle missing order

Multiple Events
===============

Subscribe to several signals in the same module:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import (
        paystack_payment_successful,
        paystack_subscription_created,
        paystack_transfer_successful,
        paystack_refund_processed,
        paystack_dispute_created,
        paystack_invoice_created,
        paystack_customeridentification_success,
    )

    @receiver(paystack_payment_successful)
    def on_payment(sender, transaction_data, **kwargs):
        ...

    @receiver(paystack_subscription_created)
    def on_subscription(sender, subscription_data, **kwargs):
        ...

    @receiver(paystack_transfer_successful)
    def on_transfer(sender, transfer_data, **kwargs):
        ...

    @receiver(paystack_refund_processed)
    def on_refund(sender, refund_data, **kwargs):
        ...

    @receiver(paystack_dispute_created)
    def on_dispute(sender, dispute_data, **kwargs):
        ...

    @receiver(paystack_invoice_created)
    def on_invoice(sender, invoice_data, **kwargs):
        ...

    @receiver(paystack_customeridentification_success)
    def on_customer_verified(sender, identification_data, **kwargs):
        ...

Disabling Signals
=================

Set ``ENABLE_SIGNALS`` to ``False`` to suppress all signal dispatch:

.. code-block:: python

    PAYSTACK = {
        'SECRET_KEY': 'sk_...',
        'ENABLE_SIGNALS': False,
    }

Best Practices
==============

1. **Keep handlers fast** — Offload long-running work to Celery or Django-Q.
2. **Use try/except** — A failing handler should not crash the webhook response.
3. **Test in isolation** — Send signals manually in unit tests:

   .. code-block:: python

       from djpaystack.signals import paystack_payment_successful

       paystack_payment_successful.send(
           sender=None,
           transaction_data={'reference': 'test_ref', 'amount': 50000},
       )

4. **Log signal events** — Helps diagnose missed or double-processed payments.
