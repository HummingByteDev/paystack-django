.. _customers:

Customers
=========

Manage customer information with the Customers API.

Creating a Customer
-------------------

.. code-block:: python

    from djpaystack.api.customers import Customer

    customer = Customer()
    response = customer.create(
        email='customer@example.com',
        first_name='John',
        last_name='Doe',
        phone='9012345678',
        metadata={
            'customer_id': 123,
            'registration_date': '2024-01-15'
        }
    )

    if response['status']:
        customer_id = response['data']['customer_code']

Listing Customers
-----------------

.. code-block:: python

    from djpaystack.api.customers import Customer

    customer = Customer()
    response = customer.list(page=1, per_page=50)

    if response['status']:
        customers = response['data']
        for cust in customers:
            print(f"{cust['email']} - {cust['first_name']}")

Getting Customer Details
------------------------

.. code-block:: python

    from djpaystack.api.customers import Customer

    customer = Customer()
    response = customer.fetch(customer_id=12345)

    if response['status']:
        customer_data = response['data']

Updating a Customer
-------------------

.. code-block:: python

    from djpaystack.api.customers import Customer

    customer = Customer()
    response = customer.update(
        code=customer_code,
        first_name='Jane',
        last_name='Smith',
        phone='9112345678'
    )

For more details, see the :ref:`api/customers` reference.
