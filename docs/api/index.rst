.. _api/index:

API Reference
=============

paystack-django provides 26 API modules, all accessible from ``PaystackClient``:

.. code-block:: python

    from djpaystack import PaystackClient

    client = PaystackClient()
    # or as a context manager:
    with PaystackClient() as client:
        ...

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Attribute
     - Class
     - Description
   * - ``client.transactions``
     - ``TransactionAPI``
     - Initialize, verify, list, charge authorizations
   * - ``client.customers``
     - ``CustomerAPI``
     - Create, fetch, validate, risk actions
   * - ``client.plans``
     - ``PlanAPI``
     - Create and manage subscription plans
   * - ``client.subscriptions``
     - ``SubscriptionAPI``
     - Create, enable, disable subscriptions
   * - ``client.charge``
     - ``ChargeAPI``
     - Card, bank transfer, USSD, QR, EFT charges
   * - ``client.dedicated_accounts``
     - ``DedicatedAccountAPI``
     - Dedicated Virtual Accounts (DVA)
   * - ``client.direct_debit``
     - ``DirectDebitAPI``
     - Direct debit authorizations
   * - ``client.transfers``
     - ``TransferAPI``
     - Initiate, finalize, list transfers
   * - ``client.transfer_recipients``
     - ``TransferRecipientAPI``
     - Manage transfer recipients
   * - ``client.transfer_control``
     - ``TransferControlAPI``
     - Enable/disable OTP, resend OTP
   * - ``client.refunds``
     - ``RefundAPI``
     - Create, list, fetch, retry refunds
   * - ``client.disputes``
     - ``DisputeAPI``
     - List, fetch, manage disputes
   * - ``client.splits``
     - ``SplitAPI``
     - Transaction split groups
   * - ``client.subaccounts``
     - ``SubaccountAPI``
     - Manage subaccounts
   * - ``client.products``
     - ``ProductAPI``
     - Create and manage products
   * - ``client.pages``
     - ``PageAPI``
     - Payment pages
   * - ``client.payment_requests``
     - ``PaymentRequestAPI``
     - Invoice / payment requests
   * - ``client.settlements``
     - ``SettlementAPI``
     - Settlement data
   * - ``client.bulk_charges``
     - ``BulkChargeAPI``
     - Batch charge operations
   * - ``client.terminal``
     - ``TerminalAPI``
     - POS terminal operations
   * - ``client.virtual_terminal``
     - ``VirtualTerminalAPI``
     - Virtual terminal payments
   * - ``client.apple_pay``
     - ``ApplePayAPI``
     - Apple Pay domain registration
   * - ``client.verification``
     - ``VerificationAPI``
     - BVN, account verification
   * - ``client.integration``
     - ``IntegrationAPI``
     - Integration timeout settings
   * - ``client.miscellaneous``
     - ``MiscellaneousAPI``
     - Banks list, countries, etc.

Base Client
-----------

.. autoclass:: djpaystack.api.base.BaseAPI
   :members:
   :undoc-members:

Detailed API pages
------------------

.. toctree::
   :maxdepth: 1

   transactions
   customers
   subscriptions
   payments
   refunds
   transfers
   verification
   dedicated_accounts
   direct_debit
   disputes
   splits
   terminal
   miscellaneous
