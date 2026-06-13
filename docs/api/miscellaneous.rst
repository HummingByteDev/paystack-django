.. _api/miscellaneous:

Miscellaneous API
=================

Utility endpoints: bank lists, countries, and more.

.. automodule:: djpaystack.api.miscellaneous
   :members:
   :undoc-members:
   :show-inheritance:

Integration API
---------------

.. automodule:: djpaystack.api.integration
   :members:
   :undoc-members:
   :show-inheritance:

Bulk Charges API
----------------

.. automodule:: djpaystack.api.bulk_charges
   :members:
   :undoc-members:
   :show-inheritance:

Products API
------------

.. automodule:: djpaystack.api.products
   :members:
   :undoc-members:
   :show-inheritance:

Settlements API
---------------

.. automodule:: djpaystack.api.settlements
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Miscellaneous
    client.miscellaneous.list_banks(country='nigeria', currency='NGN')
    client.miscellaneous.list_countries()
    client.miscellaneous.list_states(country='NG')

    # Integration
    client.integration.fetch_payment_session_timeout()
    client.integration.update_payment_session_timeout(timeout=30)

    # Bulk charges
    client.bulk_charges.initiate(charges=[...])
    client.bulk_charges.list()
    client.bulk_charges.fetch(id_or_code=...)
    client.bulk_charges.fetch_charges_in_batch(id_or_code=...)
    client.bulk_charges.pause(batch_code=...)
    client.bulk_charges.resume(batch_code=...)

    # Products
    client.products.create(name=..., description=..., price=..., currency=...)
    client.products.list()
    client.products.fetch(id=...)
    client.products.update(id=..., name=...)

    # Settlements
    client.settlements.list()
    client.settlements.fetch_transactions(id=...)
