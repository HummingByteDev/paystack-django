.. _api/transactions:

Transactions API
================

.. automodule:: djpaystack.api.transactions
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Initialize (with optional dynamic split)
    client.transactions.initialize(email=..., amount=..., split={...})

    # Verify
    client.transactions.verify(reference=...)

    # Charge saved authorization (with optional split_code)
    client.transactions.charge_authorization(
        authorization_code=..., email=..., amount=...,
        split_code=..., callback_url=...,
    )

    # List / Fetch / Timeline / Export / Totals
    client.transactions.list(page=1, per_page=50)
    client.transactions.fetch(id=...)
    client.transactions.timeline(id_or_reference=...)
    client.transactions.export(from_=..., to=...)
    client.transactions.totals()
