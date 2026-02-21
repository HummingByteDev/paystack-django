.. paystack-django documentation master file

====================================================
paystack-django: Django Paystack Payment Integration
====================================================

**paystack-django** is a comprehensive Django integration for the `Paystack Payment Gateway <https://paystack.com>`_.
It provides 26 API modules, Django models, webhook handling with signature verification,
Django signals, and production-ready defaults — everything you need to accept payments in your Django application.

.. image:: https://badge.fury.io/py/paystack-django.svg
   :target: https://badge.fury.io/py/paystack-django

.. image:: https://img.shields.io/badge/Django-3.2%2B-green
   :target: https://www.djangoproject.com

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue
   :target: https://www.python.org

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

**Highlights:**

- **26 API modules** — Transactions, Customers, Charge, Plans, Subscriptions, Transfers, Refunds, Disputes, Dedicated Accounts, Direct Debit, Splits, Subaccounts, Products, Pages, Payment Requests, Settlements, Bulk Charges, Terminal, Virtual Terminal, Apple Pay, Verification, Integration, Miscellaneous, Transfer Recipients, Transfer Control
- **Django Models** — ``PaystackTransaction``, ``PaystackCustomer``, ``PaystackPlan``, ``PaystackSubscription``, ``PaystackTransfer``, ``PaystackWebhookEvent``
- **Webhook System** — Signature-verified, IP-whitelisted, deduplicated event handling
- **Django Signals** — 9 signals for payment lifecycle events
- **System Checks** — Validates configuration at startup (``E001``)
- **Context Manager** — ``PaystackClient`` supports ``with`` statements
- **Management Commands** — ``paystack_listen`` (Cloudflare Tunnel) and ``paystack_webhook_event`` (test events)
- **Type Hints** — Fully typed with ``py.typed`` marker

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
   api/transactions
   api/customers
   api/subscriptions
   api/payments
   api/refunds
   api/transfers
   api/verification
   api/dedicated_accounts
   api/direct_debit
   api/disputes
   api/splits
   api/terminal
   api/miscellaneous

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   advanced/webhook_security
   advanced/cloudflare_tunnel
   advanced/local_webhook_testing
   advanced/signals
   advanced/testing
   advanced/webhooks
   advanced/models

.. toctree::
   :maxdepth: 2
   :caption: Project

   changelog
   contributing
   troubleshooting

Quick Example
=============

.. code-block:: python

   from djpaystack import PaystackClient

   with PaystackClient() as client:
       # Initialize a payment
       response = client.transactions.initialize(
           email='customer@example.com',
           amount=50000,  # 500 NGN in kobo
       )
       print(response['data']['authorization_url'])

       # Verify after payment
       result = client.transactions.verify(reference=response['data']['reference'])
       if result['data']['status'] == 'success':
           print('Payment confirmed!')

Supported Services
==================

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Category
     - API Modules
   * - **Payments**
     - Transactions, Charge, Payment Requests, Pages
   * - **Customers**
     - Customers, Direct Debit, Dedicated Accounts
   * - **Recurring**
     - Plans, Subscriptions
   * - **Payouts**
     - Transfers, Transfer Recipients, Transfer Control
   * - **Commerce**
     - Products, Splits, Subaccounts
   * - **Operations**
     - Refunds, Disputes, Settlements, Bulk Charges
   * - **Other**
     - Verification, Terminal, Virtual Terminal, Apple Pay, Integration, Miscellaneous

Resources
=========

- `GitHub Repository <https://github.com/HummingByteDev/paystack-django>`_
- `PyPI Package <https://pypi.org/project/paystack-django/>`_
- `Paystack Official Documentation <https://paystack.com/docs>`_
- `Report Issues <https://github.com/HummingByteDev/paystack-django/issues>`_

License
=======

MIT License — see the `LICENSE <https://github.com/HummingByteDev/paystack-django/blob/main/LICENSE>`_ file.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
