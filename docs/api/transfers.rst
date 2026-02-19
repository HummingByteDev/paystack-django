.. _api/transfers:

Transfers API
=============

Transfer Recipients
-------------------

.. automodule:: djpaystack.api.transfer_recipients
   :members:
   :undoc-members:
   :show-inheritance:

Transfers
---------

.. automodule:: djpaystack.api.transfers
   :members:
   :undoc-members:
   :show-inheritance:

Transfer Control
----------------

.. automodule:: djpaystack.api.transfer_control
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Create recipient
    client.transfer_recipients.create(
        type='nuban', name='John Doe',
        account_number='0123456789', bank_code='058',
    )

    # Initiate transfer
    client.transfers.initiate(
        source='balance', amount=100000,
        recipient='RCP_xxxxx', reason='Payout',
    )

    # Finalize (if OTP required)
    client.transfers.finalize(transfer_code='TRF_xxxxx', otp='123456')

    # Bulk transfer
    client.transfers.bulk(
        source='balance',
        transfers=[
            {'amount': 50000, 'recipient': 'RCP_xxx', 'reference': 'ref-1'},
            {'amount': 75000, 'recipient': 'RCP_yyy', 'reference': 'ref-2'},
        ],
    )

    # Transfer control
    client.transfer_control.check_balance()
    client.transfer_control.enable_otp()
    client.transfer_control.disable_otp()
    client.transfer_control.resend_otp(transfer_code=..., reason=...)
