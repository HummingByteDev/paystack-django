.. _api/direct_debit:

Direct Debit API
================

Manage direct debit authorizations for recurring payments via bank accounts.

.. automodule:: djpaystack.api.direct_debit
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Initialize authorization (sends OTP to customer)
    client.direct_debit.initialize_authorization(
        email='customer@example.com',
        bank_code='058',
        account_number='0123456789',
    )

    # Verify with OTP
    client.direct_debit.verify_authorization(reference='ref-from-init')

    # Activation charge (small debit to activate)
    client.direct_debit.activation_charge(customer_id='CUS_xxxxx')

    # Bulk activation charge
    client.direct_debit.bulk_activation_charge(customer_ids=['CUS_xxx', 'CUS_yyy'])

Webhook Events
--------------

- ``direct_debit.authorization.created`` — Authorization created
- ``direct_debit.authorization.active`` — Authorization activated and ready for use
