.. _api/payments:

Payments & Charges
==================

Charge API
----------

.. automodule:: djpaystack.api.charge
   :members:
   :undoc-members:
   :show-inheritance:

Supports card, bank, USSD, mobile money, bank transfer, EFT (South Africa), and QR code channels:

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Bank transfer (Pay with Transfer)
    client.charge.create(
        email='customer@example.com',
        amount=50000,
        bank_transfer={'account_expires_at': '2025-12-31T23:59:59'},
    )

    # QR code (scan-to-pay)
    client.charge.create(
        email='customer@example.com',
        amount=50000,
        qr={'provider': 'visa'},
    )

    # EFT (South Africa / Ozow)
    client.charge.create(
        email='customer@example.com',
        amount=50000,
        eft={'provider': 'ozow'},
    )

    # Submit PIN / OTP / Phone / Birthday / Address
    client.charge.submit_pin(reference=..., pin=...)
    client.charge.submit_otp(reference=..., otp=...)
    client.charge.submit_phone(reference=..., phone=...)
    client.charge.submit_birthday(reference=..., birthday=...)
    client.charge.submit_address(reference=..., address=..., city=..., state=..., zipcode=...)

    # Check pending charge
    client.charge.check_pending(reference=...)

Payment Requests API
--------------------

.. automodule:: djpaystack.api.payment_requests
   :members:
   :undoc-members:
   :show-inheritance:

.. code-block:: python

    client.payment_requests.create(customer=..., amount=..., description=...)
    client.payment_requests.list()
    client.payment_requests.fetch(id_or_code=...)
    client.payment_requests.send_notification(id_or_code=...)
    client.payment_requests.verify(code=...)

Pages API
---------

.. code-block:: python

    client.pages.create(name=..., amount=..., description=...)
    client.pages.list()
    client.pages.fetch(id_or_slug=...)
    client.pages.update(id_or_slug=..., name=...)
    client.pages.check_slug_availability(slug=...)
