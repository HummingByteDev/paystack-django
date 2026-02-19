.. _subscriptions:

Subscriptions
=============

Manage recurring payments with Plans and Subscriptions.

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

Plans
-----

Create a Plan
~~~~~~~~~~~~~

.. code-block:: python

    response = client.plans.create(
        name='Monthly Pro',
        amount=500000,       # 5,000 NGN
        interval='monthly',  # daily, weekly, monthly, quarterly, biannually, annually
        description='Pro plan with all features',
    )
    plan_code = response['data']['plan_code']

List / Fetch Plans
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.plans.list(page=1, per_page=50)
    response = client.plans.fetch(id_or_code=plan_code)

Update a Plan
~~~~~~~~~~~~~

.. code-block:: python

    response = client.plans.update(
        id_or_code=plan_code,
        name='Monthly Pro v2',
        amount=600000,
    )

Subscriptions
-------------

Create a Subscription
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.subscriptions.create(
        customer='CUS_xxxxx',
        plan=plan_code,
        authorization='AUTH_xxxxx',
    )
    sub_code = response['data']['subscription_code']

List / Fetch Subscriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.subscriptions.list()
    response = client.subscriptions.fetch(id_or_code=sub_code)

Enable / Disable
~~~~~~~~~~~~~~~~

.. code-block:: python

    response = client.subscriptions.enable(code=sub_code, token=email_token)
    response = client.subscriptions.disable(code=sub_code, token=email_token)

Generate Update Link
~~~~~~~~~~~~~~~~~~~~

Send the customer a link to update their card details:

.. code-block:: python

    response = client.subscriptions.generate_update_link(code=sub_code)
    link = response['data']['link']

Webhook Events
--------------

Subscription-related webhook events:

- ``subscription.create`` — New subscription created
- ``subscription.disable`` — Subscription disabled
- ``subscription.not_renew`` — Subscription will not renew
- ``subscription.expiring_cards`` — Cards about to expire
- ``invoice.create`` — Invoice created for subscription
- ``invoice.payment_failed`` — Subscription payment failed

Listen via Django signals:

.. code-block:: python

    from django.dispatch import receiver
    from djpaystack.signals import paystack_subscription_created, paystack_subscription_cancelled

    @receiver(paystack_subscription_created)
    def on_sub_created(sender, transaction_data, **kwargs):
        print(f"New subscription: {transaction_data}")

    @receiver(paystack_subscription_cancelled)
    def on_sub_cancelled(sender, transaction_data, **kwargs):
        print(f"Subscription cancelled: {transaction_data}")
