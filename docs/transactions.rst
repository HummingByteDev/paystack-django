.. _transactions:

Transactions
============

The Transactions API is the core of paystack-django. Use it to initialize payments,
verify transactions, charge saved authorizations, and more.

Overview
--------

A Paystack transaction represents a single payment attempt. Key attributes:

- **reference** — Unique identifier you provide (or Paystack auto-generates one)
- **amount** — In **kobo** (100 kobo = 1 NGN)
- **status** — ``pending``, ``success``, ``failed``, or ``abandoned``
- **authorization_url** — Hosted payment page URL

All examples below use ``PaystackClient``:

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

Initialize a Transaction
------------------------

.. code-block:: python

    response = client.transactions.initialize(
        email='customer@example.com',
        amount=50000,           # 500 NGN
        reference='order-001',  # optional
        currency='NGN',         # optional, default NGN
        metadata={'order_id': 42},
    )

    auth_url = response['data']['authorization_url']
    # Redirect user to auth_url

**Dynamic Split** — split the payment on-the-fly without a pre-created split group:

.. code-block:: python

    response = client.transactions.initialize(
        email='customer@example.com',
        amount=100000,
        split={
            'type': 'percentage',
            'bearer_type': 'account',
            'subaccounts': [
                {'subaccount': 'ACCT_xxx', 'share': 30},
                {'subaccount': 'ACCT_yyy', 'share': 20},
            ],
        },
    )

Verify a Transaction
--------------------

After the user completes (or abandons) the payment:

.. code-block:: python

    response = client.transactions.verify(reference='order-001')

    data = response['data']
    if data['status'] == 'success':
        print(f"Paid {data['amount']} kobo via {data['channel']}")

List Transactions
-----------------

.. code-block:: python

    response = client.transactions.list(page=1, per_page=50)
    response = client.transactions.list(status='success', from_='2025-01-01', to='2025-06-01')

Fetch a Single Transaction
--------------------------

.. code-block:: python

    response = client.transactions.fetch(id=123456)

Charge Authorization (Recurring)
---------------------------------

If you have a saved ``authorization_code``, charge the customer again:

.. code-block:: python

    response = client.transactions.charge_authorization(
        authorization_code='AUTH_xxxxx',
        email='customer@example.com',
        amount=50000,
        reference='renewal-001',
        split_code='SPL_xxxxx',   # optional
        callback_url='https://example.com/callback',  # optional
    )

Transaction Timeline
--------------------

.. code-block:: python

    response = client.transactions.timeline(id_or_reference='order-001')

Export Transactions
-------------------

.. code-block:: python

    response = client.transactions.export(from_='2025-01-01', to='2025-06-30')

Transaction Totals
------------------

.. code-block:: python

    response = client.transactions.totals()

Error Handling
--------------

.. code-block:: python

    from djpaystack.exceptions import PaystackAPIError, PaystackNetworkError

    try:
        response = client.transactions.verify(reference='bad-ref')
    except PaystackAPIError as e:
        print(f"API error: {e}")
    except PaystackNetworkError:
        print("Network issue — retried automatically")

Amount Conversion
-----------------

Use the built-in helper for safe naira-to-kobo conversion:

.. code-block:: python

    from djpaystack.utils import naira_to_kobo

    amount = naira_to_kobo(500.50)  # 50050 (uses Decimal internally)
