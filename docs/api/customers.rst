.. _api/customers:

Customers API
=============

.. automodule:: djpaystack.api.customers
   :members:
   :undoc-members:
   :show-inheritance:

Example Usage
-------------

.. code-block:: python

    from djpaystack.api.customers import Customer

    customer = Customer()
    
    # Create
    response = customer.create(
        email='customer@example.com',
        first_name='John',
        last_name='Doe'
    )
    
    # List
    response = customer.list()
    
    # Fetch
    response = customer.fetch(customer_id=123)
    
    # Update
    response = customer.update(
        code='CUST_123',
        first_name='Jane'
    )
