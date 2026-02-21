.. _advanced/webhook_security:

================
Webhook Security
================

Paystack uses **HMAC SHA-512** signatures to prove that a webhook request
genuinely originated from their servers. paystack-django verifies these
signatures automatically — all you need is a valid ``PAYSTACK['SECRET_KEY']``.

Why ``SECRET_KEY`` and not a separate webhook secret?
=====================================================

Paystack computes the webhook signature using your **API secret key**
(the same ``sk_live_...`` or ``sk_test_...`` key you use for API calls).
There is no separate "webhook secret" in Paystack's architecture.

paystack-django therefore uses ``PAYSTACK['SECRET_KEY']`` for both:

1. Authenticating outbound API requests (``Authorization: Bearer sk_...``).
2. Verifying inbound webhook signatures (``X-Paystack-Signature`` header).

This simplifies configuration — one key to manage instead of two.

.. code-block:: python

   # settings.py — this is all you need
   PAYSTACK = {
       'SECRET_KEY': 'sk_live_xxxxxxxxxxxxxxxx',
       'PUBLIC_KEY': 'pk_live_xxxxxxxxxxxxxxxx',
   }

.. important::

   If you previously configured ``PAYSTACK['WEBHOOK_SECRET']``, you can
   safely remove it. As of v1.2.0 that setting is ignored.
   Webhook verification now uses ``SECRET_KEY`` exclusively.

How HMAC SHA-512 Verification Works
====================================

When Paystack sends a webhook, it:

1. Takes the **raw JSON body** of the POST request.
2. Computes ``HMAC-SHA512(body, your_secret_key)``.
3. Sends the hex digest in the ``X-Paystack-Signature`` HTTP header.

paystack-django reproduces the same computation on your server:

.. code-block:: python

   import hmac, hashlib

   computed = hmac.new(
       secret_key.encode('utf-8'),
       request.body,          # raw bytes
       hashlib.sha512,
   ).hexdigest()

   is_valid = hmac.compare_digest(computed, request_signature)

If the two digests match, the payload is authentic and untampered.
``hmac.compare_digest`` is used (instead of ``==``) to prevent timing attacks.

Request Flow
============

.. code-block:: text

         ┌────────────┐             ┌──────────────────┐
         │  Paystack   │  POST      │  Your Django App  │
         │  Servers    │ ─────────► │  /paystack/webhook/│
         └────────────┘             └──────────────────┘
                │                           │
     1. JSON body                  2. Read X-Paystack-Signature
     2. HMAC-SHA512(body, sk_...)  3. HMAC-SHA512(body, sk_...)
     3. Attach as header           4. compare_digest()
                                   5. If valid → process event
                                      If invalid → 400 Bad Request

Additional Layers
=================

IP Whitelisting
---------------

Paystack sends webhooks from a known set of IPs. By default paystack-django
allows these IPs:

- ``52.31.139.75``
- ``52.49.173.169``
- ``52.214.14.220``

You can override the whitelist:

.. code-block:: python

   PAYSTACK = {
       'SECRET_KEY': 'sk_...',
       'ALLOWED_WEBHOOK_IPS': ['52.31.139.75', '52.49.173.169', '52.214.14.220'],
   }

Set to an empty list to use the default Paystack IPs.

Event Deduplication
-------------------

Paystack may retry webhook delivery. paystack-django tracks processed event
IDs in an ``OrderedDict`` (in-memory, capped at 1 000 entries) and
optionally in the ``PaystackWebhookEvent`` database model, preventing
double-processing.

HTTPS in Production
-------------------

Paystack **requires** HTTPS for webhook URLs in production. During local
development, the ``paystack_listen`` command provides an HTTPS tunnel
automatically via Cloudflare.

Best Practices
==============

1. **Never expose ``SECRET_KEY`` in client-side code or version control.**
   Use environment variables:

   .. code-block:: python

      import os
      PAYSTACK = {
          'SECRET_KEY': os.environ['PAYSTACK_SECRET_KEY'],
      }

2. **Always verify signatures** — paystack-django does this by default;
   do not bypass it.

3. **Return 200 quickly** — Process webhook data asynchronously (e.g. with
   Celery) and return ``200 OK`` within a few seconds, or Paystack will retry.

4. **Handle retries idempotently** — Use the built-in deduplication or check
   transaction references before fulfilling orders.

5. **Monitor failures** — Check ``PaystackWebhookEvent`` records with
   ``processed=False`` for events that could not be handled.
