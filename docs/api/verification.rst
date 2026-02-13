.. _api/verification:

Verification API
================

.. automodule:: djpaystack.api.verification
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.verification import Verification

    verification = Verification()
    
    # Verify account
    response = verification.verify_account(
        account_number='0123456789',
        bank_code='057'
    )
    
    # Validate account
    response = verification.validate_account(
        account_number='0123456789',
        bank_code='057',
        account_name='John Doe'
    )
