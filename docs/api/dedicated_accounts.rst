.. _api/dedicated_accounts:

Dedicated Accounts API
======================

Dedicated Virtual Accounts (DVA) allow you to assign permanent bank account numbers
to your customers for receiving payments.

.. automodule:: djpaystack.api.dedicated_accounts
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Single-step assignment (create customer + assign account)
    client.dedicated_accounts.assign(
        email='customer@example.com',
        first_name='John',
        last_name='Doe',
        phone='+2348012345678',
        preferred_bank='wema-bank',
    )

    # Create DVA for existing customer
    client.dedicated_accounts.create(customer='CUS_xxxxx', preferred_bank='wema-bank')

    # List / Fetch
    client.dedicated_accounts.list()
    client.dedicated_accounts.fetch(dedicated_account_id=123)

    # Requery for recent transactions
    client.dedicated_accounts.requery(account_number='1234567890', provider_slug='wema-bank')

    # Split DVA payments
    client.dedicated_accounts.split(
        account_number='1234567890',
        subaccount='ACCT_xxxxx',
        split_code='SPL_xxxxx',
    )

    # Remove split
    client.dedicated_accounts.remove_split(account_number='1234567890')

    # Deactivate
    client.dedicated_accounts.deactivate(dedicated_account_id=123)

Webhook Events
--------------

- ``dedicatedaccount.assign.success`` — DVA assigned successfully
- ``dedicatedaccount.assign.failed`` — DVA assignment failed
