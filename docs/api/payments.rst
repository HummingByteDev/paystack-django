.. _api/payments:

Payments & Charges
==================

.. automodule:: djpaystack.api.charge
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: djpaystack.api.payment_requests
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.charge import Charge
    from djpaystack.api.payment_requests import PaymentRequest

    # Charge
    charge = Charge()
    response = charge.create(
        authorization_code='AUTH_123',
        email='customer@example.com',
        amount=50000
    )

    # Payment Request
    payment_request = PaymentRequest()
    response = payment_request.create(
        customer='CUST_123',
        amount=50000
    )
