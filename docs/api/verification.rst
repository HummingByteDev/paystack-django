.. _api/verification:

Verification API
================

.. automodule:: djpaystack.api.verification
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Resolve account number
    client.verification.resolve_account(
        account_number='0123456789',
        bank_code='058',
    )

    # Validate account
    client.verification.validate_account(
        account_name='John Doe',
        account_number='0123456789',
        account_type='personal',
        bank_code='058',
        country_code='NG',
        document_type='identityNumber',
        document_number='12345678901',
    )

    # Resolve card BIN
    client.verification.resolve_card_bin(bin='539983')
