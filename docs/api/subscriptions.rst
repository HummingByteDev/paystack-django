.. _api/subscriptions:

Subscriptions & Plans API
=========================

Plans
-----

.. automodule:: djpaystack.api.plans
   :members:
   :undoc-members:
   :show-inheritance:

Subscriptions
-------------

.. automodule:: djpaystack.api.subscriptions
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Plans
    client.plans.create(name=..., amount=..., interval=...)
    client.plans.list()
    client.plans.fetch(id_or_code=...)
    client.plans.update(id_or_code=..., name=..., amount=...)

    # Subscriptions
    client.subscriptions.create(customer=..., plan=..., authorization=...)
    client.subscriptions.list()
    client.subscriptions.fetch(id_or_code=...)
    client.subscriptions.enable(code=..., token=...)
    client.subscriptions.disable(code=..., token=...)
    client.subscriptions.generate_update_link(code=...)
