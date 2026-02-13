.. _api/refunds:

Refunds API
===========

.. automodule:: djpaystack.api.refunds
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.refunds import Refund

    refund = Refund()
    
    # Create refund
    response = refund.create(
        transaction=transaction_id,
        amount=50000,
        notes='Customer requested refund'
    )
    
    # List refunds
    response = refund.list()
    
    # Fetch specific refund
    response = refund.fetch(refund_reference)
