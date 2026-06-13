.. _customers:

Customers
=========

Manage customer records, validate identities, and control risk actions.

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

Create a Customer
-----------------

.. code-block:: python

    response = client.customers.create(
        email='customer@example.com',
        first_name='John',
        last_name='Doe',
        phone='2348012345678',
        metadata={'source': 'web'},
    )
    customer_code = response['data']['customer_code']

List Customers
--------------

.. code-block:: python

    response = client.customers.list(page=1, per_page=50)

Fetch a Customer
----------------

.. code-block:: python

    response = client.customers.fetch(email_or_code='CUS_xxxxx')

Update a Customer
-----------------

.. code-block:: python

    response = client.customers.update(
        code='CUS_xxxxx',
        first_name='Jane',
        last_name='Smith',
    )

Validate a Customer
-------------------

Submit identity information (BVN, bank account) for validation:

.. code-block:: python

    response = client.customers.validate(
        code='CUS_xxxxx',
        first_name='John',
        last_name='Doe',
        type='bank_account',
        value='0123456789',
        country='NG',
        bvn='12345678901',
        bank_code='058',
        account_number='0123456789',
    )

Risk Action
-----------

Whitelist or blacklist a customer:

.. code-block:: python

    # Whitelist
    response = client.customers.set_risk_action(
        customer='CUS_xxxxx',
        risk_action='allow',
    )

    # Blacklist
    response = client.customers.set_risk_action(
        customer='CUS_xxxxx',
        risk_action='deny',
    )

Deactivate Authorization
------------------------

.. code-block:: python

    response = client.customers.deactivate_authorization(
        authorization_code='AUTH_xxxxx',
    )

Django Model
------------

Customers are automatically saved when webhooks arrive (if ``ENABLE_MODELS`` is ``True``):

.. code-block:: python

    from djpaystack.models import PaystackCustomer

    customer = PaystackCustomer.objects.get(customer_code='CUS_xxxxx')
    print(customer.email, customer.first_name)
