.. _api/subscriptions:

Subscriptions API
=================

.. automodule:: djpaystack.api.subscriptions
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.subscriptions import Subscription

    subscription = Subscription()
    
    # Create
    response = subscription.create(
        customer='CUST_123',
        plan='PLN_123',
        authorization='AUTH_123'
    )
    
    # List
    response = subscription.list()
    
    # Enable
    response = subscription.enable(
        code='SUB_123',
        token='token_123'
    )
    
    # Disable
    response = subscription.disable(
        code='SUB_123',
        token='token_123'
    )
