.. _api/customers:

Customers API
=============

.. automodule:: djpaystack.api.customers
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    client.customers.create(email=..., first_name=..., last_name=..., phone=...)
    client.customers.list(page=1, per_page=50)
    client.customers.fetch(email_or_code=...)
    client.customers.update(code=..., first_name=...)
    client.customers.validate(code=..., first_name=..., last_name=..., type=..., value=..., country=...)
    client.customers.set_risk_action(customer=..., risk_action='allow')  # or 'deny'
    client.customers.deactivate_authorization(authorization_code=...)
