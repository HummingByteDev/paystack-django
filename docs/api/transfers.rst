.. _api/transfers:

Transfers API
=============

.. automodule:: djpaystack.api.transfers
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: djpaystack.api.transfer_recipients
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.transfers import Transfer
    from djpaystack.api.transfer_recipients import TransferRecipient

    # Add recipient
    recipient = TransferRecipient()
    response = recipient.create(
        type='nuban',
        account_number='0123456789',
        bank_code='057',
        name='John Doe'
    )

    # Initiate transfer
    transfer = Transfer()
    response = transfer.initiate(
        source='balance',
        recipient=recipient_code,
        amount=100000,
        reference='transfer-123'
    )
