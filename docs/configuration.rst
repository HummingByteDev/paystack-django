.. _configuration:

Configuration
=============

All configuration lives in one dictionary in your Django ``settings.py``.

Minimal Setup
-------------

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'djpaystack',
    ]

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_your_secret_key',
        'PUBLIC_KEY': 'pk_test_your_public_key',
    }

Get your keys from the `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_.

Then run migrations:

.. code-block:: bash

    python manage.py migrate djpaystack

Environment Variables
---------------------

Never hard-code secrets. Use ``os.environ``, ``django-environ``, or any config loader:

.. code-block:: python

    import os

    PAYSTACK = {
        'SECRET_KEY': os.environ['PAYSTACK_SECRET_KEY'],
        'PUBLIC_KEY': os.environ['PAYSTACK_PUBLIC_KEY'],
        'WEBHOOK_SECRET': os.environ.get('PAYSTACK_WEBHOOK_SECRET', ''),
    }

Full Configuration
------------------

.. code-block:: python

    PAYSTACK = {
        # Required
        'SECRET_KEY': 'sk_...',          # Paystack secret API key
        'PUBLIC_KEY': 'pk_...',          # Paystack public API key

        # Webhook
        'WEBHOOK_SECRET': 'whsec_...',   # HMAC SHA-512 verification
        'ALLOWED_WEBHOOK_IPS': [],       # Empty = Paystack default IPs

        # API behaviour
        'BASE_URL': 'https://api.paystack.co',
        'TIMEOUT': 30,                   # Request timeout (seconds)
        'MAX_RETRIES': 3,                # Automatic retries on 429/5xx
        'VERIFY_SSL': True,
        'CURRENCY': 'NGN',
        'ENVIRONMENT': 'production',     # 'production' or 'test'

        # Features
        'AUTO_VERIFY_TRANSACTIONS': True,
        'ENABLE_SIGNALS': True,          # Send Django signals on webhooks
        'ENABLE_MODELS': True,           # Auto-save to Django models
        'CACHE_TIMEOUT': 300,            # Seconds
        'CALLBACK_URL': None,            # Default redirect URL

        # Logging
        'LOG_REQUESTS': False,
        'LOG_RESPONSES': False,
    }

Configuration Reference
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Setting
     - Purpose
     - Default
   * - ``SECRET_KEY``
     - Paystack secret API key (**required**)
     - ``None``
   * - ``PUBLIC_KEY``
     - Paystack public API key (**required**)
     - ``None``
   * - ``WEBHOOK_SECRET``
     - HMAC SHA-512 webhook signature secret
     - ``None``
   * - ``ALLOWED_WEBHOOK_IPS``
     - List of IPs to accept webhooks from. Empty list uses Paystack defaults.
     - ``[]``
   * - ``BASE_URL``
     - Paystack API base URL
     - ``https://api.paystack.co``
   * - ``TIMEOUT``
     - HTTP request timeout in seconds
     - ``30``
   * - ``MAX_RETRIES``
     - Retries on 429 / 5xx responses
     - ``3``
   * - ``VERIFY_SSL``
     - Verify SSL certificates
     - ``True``
   * - ``CURRENCY``
     - Default currency code
     - ``NGN``
   * - ``ENVIRONMENT``
     - ``'production'`` or ``'test'``
     - ``production``
   * - ``AUTO_VERIFY_TRANSACTIONS``
     - Auto-verify transactions on webhook receipt
     - ``True``
   * - ``ENABLE_SIGNALS``
     - Dispatch Django signals on webhook events
     - ``True``
   * - ``ENABLE_MODELS``
     - Persist webhook data to Django models
     - ``True``
   * - ``CACHE_TIMEOUT``
     - Cache TTL in seconds
     - ``300``
   * - ``CALLBACK_URL``
     - Default callback URL for transactions
     - ``None``
   * - ``LOG_REQUESTS``
     - Log outgoing API requests
     - ``False``
   * - ``LOG_RESPONSES``
     - Log API responses
     - ``False``

System Checks
-------------

On startup, ``djpaystack`` registers two Django system checks:

- **djpaystack.E001** — ``PAYSTACK['SECRET_KEY']`` is missing (error, blocks startup).
- **djpaystack.W001** — ``PAYSTACK['WEBHOOK_SECRET']`` is missing (warning).

Webhook Setup
-------------

1. Add the endpoint to ``urls.py``:

   .. code-block:: python

       from django.urls import path
       from djpaystack.webhooks.views import handle_webhook

       urlpatterns = [
           path('webhooks/paystack/', handle_webhook, name='paystack-webhook'),
       ]

2. In the `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_,
   set your webhook URL to ``https://yourdomain.com/webhooks/paystack/`` and copy the
   webhook secret into ``PAYSTACK['WEBHOOK_SECRET']``.

Logging
-------

All log output uses the ``djpaystack`` logger name:

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'paystack': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'paystack.log',
            },
        },
        'loggers': {
            'djpaystack': {
                'handlers': ['paystack'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

Environment-Specific Examples
-----------------------------

**Development:**

.. code-block:: python

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_...',
        'PUBLIC_KEY': 'pk_test_...',
        'LOG_REQUESTS': True,
        'LOG_RESPONSES': True,
    }

**Production:**

.. code-block:: python

    import os

    PAYSTACK = {
        'SECRET_KEY': os.environ['PAYSTACK_SECRET_KEY'],
        'PUBLIC_KEY': os.environ['PAYSTACK_PUBLIC_KEY'],
        'WEBHOOK_SECRET': os.environ['PAYSTACK_WEBHOOK_SECRET'],
        'ENVIRONMENT': 'production',
    }
