.. _api/splits:

Splits & Subaccounts API
========================

Transaction Splits
------------------

.. automodule:: djpaystack.api.splits
   :members:
   :undoc-members:
   :show-inheritance:

Subaccounts
-----------

.. automodule:: djpaystack.api.subaccounts
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # --- Splits ---
    client.splits.create(
        name='E-commerce split',
        type='percentage',
        currency='NGN',
        subaccounts=[
            {'subaccount': 'ACCT_xxx', 'share': 30},
            {'subaccount': 'ACCT_yyy', 'share': 20},
        ],
        bearer_type='account',
    )
    client.splits.list()
    client.splits.fetch(id='SPL_xxxxx')
    client.splits.update(id='SPL_xxxxx', name='Updated split')
    client.splits.add_subaccount(id='SPL_xxxxx', subaccount='ACCT_zzz', share=10)
    client.splits.remove_subaccount(id='SPL_xxxxx', subaccount='ACCT_zzz')

    # --- Subaccounts ---
    client.subaccounts.create(
        business_name='Partner Store',
        settlement_bank='058',
        account_number='0123456789',
        percentage_charge=20,
    )
    client.subaccounts.list()
    client.subaccounts.fetch(id_or_code='ACCT_xxxxx')
    client.subaccounts.update(id_or_code='ACCT_xxxxx', percentage_charge=25)

Dynamic Splits
--------------

You can also create a one-time split at transaction initialization time
(no pre-created split group required):

.. code-block:: python

    client.transactions.initialize(
        email='customer@example.com',
        amount=100000,
        split={
            'type': 'percentage',
            'bearer_type': 'account',
            'subaccounts': [
                {'subaccount': 'ACCT_xxx', 'share': 30},
            ],
        },
    )
