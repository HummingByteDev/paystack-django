.. _advanced/signals:

Django Signals
==============

paystack-django sends Django signals for payment events, allowing you to hook into the payment lifecycle.

Available Signals
-----------------

**paystack_charge_success**

Sent when a payment is successful:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_charge_success

    @receiver(paystack_charge_success)
    def on_payment_success(sender, transaction=None, **kwargs):
        """Handle successful payment"""
        print(f"Payment successful: {transaction.reference}")

**paystack_charge_failed**

Sent when a payment fails:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_charge_failed

    @receiver(paystack_charge_failed)
    def on_payment_failed(sender, transaction=None, **kwargs):
        """Handle failed payment"""
        print(f"Payment failed: {transaction.reference}")

**paystack_charge_pending**

Sent when a payment is pending:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_charge_pending

    @receiver(paystack_charge_pending)
    def on_payment_pending(sender, transaction=None, **kwargs):
        """Handle pending payment"""
        print(f"Payment pending: {transaction.reference}")

Registering Signals
-------------------

In your Django app's ``apps.py``:

.. code-block:: python

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'myapp'
        
        def ready(self):
            import myapp.signals

In your ``signals.py``:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_charge_success
    from .models import Order

    @receiver(paystack_charge_success)
    def update_order_status(sender, transaction=None, **kwargs):
        """Update order status after payment"""
        order = Order.objects.get(reference=transaction.reference)
        order.status = 'paid'
        order.paid_at = timezone.now()
        order.save()

Using Signals for Multiple Events
----------------------------------

.. code-block:: python

    from django.dispatch import receiver
    from django.db.models.signals import post_save
    from djpaystack.models import Transaction
    from djpaystack.signals import paystack_charge_success

    # On Paystack transaction model save
    @receiver(post_save, sender=Transaction)
    def on_transaction_save(sender, instance, created, **kwargs):
        if created:
            print(f"New transaction: {instance.reference}")

    # On custom signal
    @receiver(paystack_charge_success)
    def on_charge_success(sender, transaction=None, **kwargs):
        # Send confirmation email
        send_payment_confirmation_email(transaction.email)

Best Practices
--------------

1. Keep signal handlers fast - offload long operations to Celery
2. Use try-except blocks to avoid crashing signal chain
3. Log signal events for debugging
4. Test signals in isolation
5. Document custom signals

.. code-block:: python

    from django.dispatch import receiver
    from django.utils import timezone
    from djpaystack.signals import paystack_charge_success
    from .tasks import send_confirmation_email

    @receiver(paystack_charge_success)
    def handle_payment_success(sender, transaction=None, **kwargs):
        try:
            # Log event
            logger.info(f"Payment success: {transaction.reference}")
            
            # Offload long operation to Celery
            send_confirmation_email.delay(transaction.id)
            
        except Exception as e:
            logger.error(f"Error handling payment: {str(e)}")
