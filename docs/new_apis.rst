.. _new_apis:

Additional APIs & Behaviour
===========================

This page covers the less-common API clients (Virtual Terminal, Direct Debit,
Orders, Storefronts, and the customer authorization/direct-debit flow) with
usage examples, the ``WEBHOOK_SECRET`` behaviour, and migration notes.

All examples assume a configured client:

.. code-block:: python

   from djpaystack import PaystackClient
   client = PaystackClient()

Virtual Terminal
----------------

Full client for the Virtual Terminal API (create, list, fetch, update,
deactivate, assign/unassign destinations, add/remove split code).

.. code-block:: python

   vt = client.virtual_terminal.create(
       name="In-store till",
       destinations=[{"target": "+2348000000000", "name": "Sales"}],
   )
   code = vt["data"]["code"]

   client.virtual_terminal.assign_destination(
       code, [{"target": "+2348111111111", "name": "Support"}]
   )
   client.virtual_terminal.add_split_code(code, "SPL_xxx")
   client.virtual_terminal.deactivate(code)

Direct Debit
------------

Account-level Direct Debit operations. Customer-scoped onboarding lives on the
Customer API (see below).

.. code-block:: python

   client.direct_debit.trigger_activation_charge(customer_ids=[123, 456])

   page = client.direct_debit.list_mandate_authorizations(status="active")
   cursor = page["meta"].get("next")

Orders
------

.. code-block:: python

   order = client.order.create(
       email="customer@example.com",
       first_name="Ada", last_name="Lovelace", phone="+2348000000000",
       currency="NGN",
       items=[{"name": "Widget", "amount": 50000, "quantity": 1}],
       shipping={"address": "1 Marina, Lagos"},
   )
   client.order.validate(order["data"]["code"])
   client.order.list(from_date="2026-01-01", to_date="2026-02-01")

Storefronts
-----------

.. code-block:: python

   sf = client.storefront.create(name="My Shop", slug="my-shop", currency="NGN")
   sid = sf["data"]["id"]
   client.storefront.add_products(sid, [101, 102])
   client.storefront.publish(sid)
   client.storefront.verify_slug("my-shop")

Customer authorizations & direct debit
--------------------------------------

The Customer client now covers the full authorization lifecycle, including the
modern direct-debit onboarding flow.

.. code-block:: python

   init = client.customers.initialize_authorization(
       email="customer@example.com", channel="direct_debit",
   )
   client.customers.verify_authorization(init["data"]["reference"])

   client.customers.initialize_direct_debit(
       "CUS_xxx",
       account={"number": "0000000000", "bank_code": "058"},
       address={"street": "1 Marina", "city": "Lagos", "state": "LA"},
   )
   client.customers.directdebit_activation_charge("CUS_xxx", "AUTH_xxx")
   client.customers.fetch_mandate_authorizations("CUS_xxx")

Other newly added endpoints
----------------------------

.. code-block:: python

   client.products.delete("PROD_xxx")
   client.refunds.retry_with_customer_details(
       "RF_xxx", {"account_number": "0000000000", "bank_code": "058"}
   )
   client.transfers.export(status="success", from_date="2026-01-01")
   client.dedicated_accounts.assign(
       email="customer@example.com", first_name="Ada", last_name="Lovelace",
       phone="+2348000000000", preferred_bank="wema-bank", country="NG",
   )
   client.transfer_control.fetch_balance_ledger(per_page=50, page=1)

Webhook secret behaviour
------------------------

Paystack signs webhook payloads with your account **secret key**. There is no
separate "webhook secret" in Paystack.

- ``WEBHOOK_SECRET`` is therefore optional and defaults to ``SECRET_KEY``.
- Set ``WEBHOOK_SECRET`` only if you need to override the signing key.
- If **no** signing key can be resolved and
  ``WEBHOOK_SIGNATURE_REQUIRED`` is ``True`` (the default), webhooks are
  **rejected** (fail closed).

.. code-block:: python

   PAYSTACK = {
       "SECRET_KEY": "sk_live_xxx",      # also used to verify webhooks
       # "WEBHOOK_SECRET": "...",        # optional override; defaults to SECRET_KEY
       "WEBHOOK_SIGNATURE_REQUIRED": True,
   }

For local development without a configured key you may temporarily disable
verification (never in production):

.. code-block:: python

   PAYSTACK = {"WEBHOOK_SIGNATURE_REQUIRED": False}

Dispute webhooks
----------------

Dispute events are now registered under their correct Paystack names
(``charge.dispute.create``, ``charge.dispute.remind``,
``charge.dispute.resolve``), so the ``paystack_dispute_created`` and
``paystack_dispute_resolved`` signals fire as expected.

Migration notes (1.0.x → 1.2.0)
-------------------------------

See the project ``CHANGELOG`` for the full list. Key points:

- **Webhooks fail closed.** Ensure ``SECRET_KEY`` (or ``WEBHOOK_SECRET``) is set;
  otherwise webhooks are rejected.
- **POST/PUT are no longer auto-retried.** Retry writes yourself using a stable
  ``reference`` so Paystack de-duplicates them.
- **``list()`` returns a single page.** Use ``iter_all()`` to stream every record.
- ``transfers.list(customer=...)`` still works as a deprecated alias for
  ``recipient``.
- The Direct Debit client targets the current endpoints; the older ``mandate/*``
  methods were removed.
- ``setup.py``/``setup.cfg`` were removed; build with ``python -m build``.
