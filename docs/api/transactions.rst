.. _api/transactions:

Transactions API
================

.. automodule:: djpaystack.api.transactions
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    
    # Initialize
    response = transaction.initialize(
        email='customer@example.com',
        amount=50000
    )
    
    # Verify
    response = transaction.verify('ref-123')
    
    # List
    response = transaction.list()
    
    # Fetch
    response = transaction.fetch(transaction_id=123)
