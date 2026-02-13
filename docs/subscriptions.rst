.. _subscriptions:

Subscriptions
=============

Manage recurring payments with the Subscriptions API.

Creating a Subscription Plan
-----------------------------

First, create a plan:

.. code-block:: python

    from djpaystack.api.plans import Plan

    plan = Plan()
    response = plan.create(
        name='Monthly Plan',
        amount=50000,  # 500 naira in kobo
        interval='monthly'
    )

    if response['status']:
        plan_code = response['data']['plan_code']

Creating a Subscription
-----------------------

.. code-block:: python

    from djpaystack.api.subscriptions import Subscription

    subscription = Subscription()
    response = subscription.create(
        customer=customer_code,
        plan=plan_code,
        authorization=authorization_code
    )

    if response['status']:
        subscription_id = response['data']['subscription_code']

Listing Subscriptions
---------------------

.. code-block:: python

    from djpaystack.api.subscriptions import Subscription

    subscription = Subscription()
    response = subscription.list()

Managing Subscriptions
----------------------

Enable, disable, or cancel subscriptions:

.. code-block:: python

    from djpaystack.api.subscriptions import Subscription

    subscription = Subscription()

    # Disable subscription
    response = subscription.disable(
        code=subscription_code,
        token=email_token
    )

    # Enable subscription
    response = subscription.enable(
        code=subscription_code,
        token=email_token
    )

For complete API reference, see :ref:`api/subscriptions`.
