.. paystack-django documentation master file, created by sphinx-quickstart.

====================================================
paystack-django: Django Paystack Payment Integration
====================================================

**paystack-django** is a comprehensive Django integration for the `Paystack Payment Gateway <https://paystack.com>`_. This package provides a complete, production-ready solution for integrating Paystack payments into your Django applications.

.. image:: https://badge.fury.io/py/paystack-django.svg
   :target: https://badge.fury.io/py/paystack-django

.. image:: https://img.shields.io/badge/Django-3.2%2B-green
   :target: https://www.djangoproject.com

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue
   :target: https://www.python.org

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

**Features:**

- **Complete Paystack API Integration** - Access all Paystack endpoints
- **Django Models** - Pre-built models for transactions, customers, plans, and more
- **Webhook Support** - Built-in webhook handling and verification
- **Signal Support** - Django signals for payment events
- **Async Ready** - Supports async operations
- **Type Hints** - Fully typed for better IDE support
- **Comprehensive Documentation** - Detailed docs and examples
- **Test Coverage** - Extensive test suite
- **Production Ready** - Used in production by multiple companies

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   configuration

.. toctree::
   :maxdepth: 2
   :caption: Usage Guide

   transactions
   customers
   subscriptions
   webhooks

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   advanced/async
   advanced/signals
   advanced/testing
   advanced/webhooks

.. toctree::
   :maxdepth: 2
   :caption: Contributing

   contributing
   troubleshooting

Quick Start
===========

Install the package:

.. code-block:: bash

   pip install paystack-django

Add to your Django settings:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'djpaystack',
   ]

   PAYSTACK = {
       'SECRET_KEY': 'your-paystack-secret-key',
       'PUBLIC_KEY': 'your-paystack-public-key',
   }

Initialize a transaction:

.. code-block:: python

   from djpaystack.api.transactions import Transaction

   transaction = Transaction()
   response = transaction.initialize(
       email='customer@example.com',
       amount=50000,  # Amount in kobo (e.g., 500 naira)
       reference='unique-reference-123'
   )

Supported Services
==================

The package supports all major Paystack services:

- **Transactions** - Create, verify, and manage transactions
- **Customers** - Create and manage customer records
- **Plans** - Create and manage subscription plans
- **Subscriptions** - Manage customer subscriptions
- **Transfers** - Handle fund transfers
- **Refunds** - Process refunds
- **Disputes** - Manage transaction disputes
- **Settlements** - Track settlement information
- **Splits** - Configure payment splits
- **Subaccounts** - Manage subaccounts
- **Products** - Create and manage products
- **Payment Requests** - Generate payment request links
- **Verification** - Bank and account verification
- **Direct Debit** - Direct debit authorization
- **Terminal** - Terminal operations
- **Apple Pay** - Apple Pay integration
- And many more...

Resources
=========

- `GitHub Repository <https://github.com/HummingByteDev/paystack-django>`_
- `PyPI Package <https://pypi.org/project/paystack-django/>`_
- `Paystack Official Documentation <https://paystack.com/docs>`_
- `Report Issues <https://github.com/HummingByteDev/paystack-django/issues>`_
- `GitHub Discussions <https://github.com/HummingByteDev/paystack-django/discussions>`_

Support
=======

- 📚 `Full Documentation <https://django-paystack.readthedocs.io>`_
- 🐛 `Report Issues on GitHub <https://github.com/HummingByteDev/paystack-django/issues>`_
- 💬 `Join Discussions <https://github.com/HummingByteDev/paystack-django/discussions>`_
- 📧 `Email Support <dev@hummingbyte.org>`_

License
=======

This project is licensed under the MIT License. See the `LICENSE <https://github.com/HummingByteDev/paystack-django/blob/main/LICENSE>`_ file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
