.. _advanced/models:

Django Models
=============

paystack-django provides 6 Django models for persisting Paystack data locally.
When ``PAYSTACK['ENABLE_MODELS']`` is ``True`` (the default), webhook handlers
automatically create/update these records.

Models Overview
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Model
     - Purpose
   * - ``PaystackTransaction``
     - Payment transactions (amount, status, reference, customer, authorization, fees, metadata)
   * - ``PaystackCustomer``
     - Customer records (email, name, phone, customer_code, risk_action)
   * - ``PaystackPlan``
     - Subscription plans (name, amount, interval, plan_code)
   * - ``PaystackSubscription``
     - Active subscriptions (subscription_code, plan_code, status, next_payment_date)
   * - ``PaystackTransfer``
     - Transfer records (transfer_code, reference, amount, recipient_code, status)
   * - ``PaystackWebhookEvent``
     - Raw webhook event log (event_type, event_id, data, processed flag)

Usage
-----

.. code-block:: python

    from djpaystack.models import (
        PaystackTransaction,
        PaystackCustomer,
        PaystackPlan,
        PaystackSubscription,
        PaystackTransfer,
        PaystackWebhookEvent,
    )

    # Successful transactions
    paid = PaystackTransaction.objects.filter(status='success')

    # Customer lookup
    customer = PaystackCustomer.objects.get(email='customer@example.com')

    # Active subscriptions
    active_subs = PaystackSubscription.objects.filter(status='active')

    # Unprocessed webhooks
    pending = PaystackWebhookEvent.objects.filter(processed=False)

Base Model
----------

All models inherit from ``PaystackBaseModel``, which provides:

- ``created_at`` — Auto-set on creation
- ``updated_at`` — Auto-set on every save

PaystackTransaction
-------------------

.. autoclass:: djpaystack.models.PaystackTransaction
   :members:
   :show-inheritance:

Key fields: ``reference`` (unique), ``amount`` (kobo), ``currency``, ``status``,
``customer_email``, ``customer_code``, ``authorization_code``, ``authorization_url``,
``access_code``, ``paid_at``, ``channel``, ``ip_address``, ``fees``, ``fees_split``,
``metadata``, ``raw_response``.

PaystackCustomer
----------------

.. autoclass:: djpaystack.models.PaystackCustomer
   :members:
   :show-inheritance:

Key fields: ``customer_code`` (unique), ``email`` (unique), ``first_name``,
``last_name``, ``phone``, ``risk_action``, ``metadata``.

PaystackPlan
------------

.. autoclass:: djpaystack.models.PaystackPlan
   :members:
   :show-inheritance:

Key fields: ``plan_code`` (unique), ``name``, ``amount``, ``interval``,
``description``, ``currency``, ``is_active``, ``metadata``.

PaystackSubscription
--------------------

.. autoclass:: djpaystack.models.PaystackSubscription
   :members:
   :show-inheritance:

Key fields: ``subscription_code`` (unique), ``customer_code``, ``plan_code``,
``amount``, ``status``, ``next_payment_date``, ``email_token``,
``authorization_code``, ``metadata``.

PaystackTransfer
----------------

.. autoclass:: djpaystack.models.PaystackTransfer
   :members:
   :show-inheritance:

Key fields: ``transfer_code`` (unique), ``reference`` (unique), ``amount``,
``currency``, ``status``, ``recipient_code``, ``reason``, ``transferred_at``,
``metadata``.

PaystackWebhookEvent
--------------------

.. autoclass:: djpaystack.models.PaystackWebhookEvent
   :members:
   :show-inheritance:

Key fields: ``event_type``, ``event_id`` (unique), ``data`` (JSON),
``processed`` (boolean), ``processing_error``, ``ip_address``, ``user_agent``.

Migrations
----------

.. code-block:: bash

    python manage.py migrate djpaystack
