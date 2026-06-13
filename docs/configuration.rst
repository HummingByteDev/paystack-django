.. _configuration:

Configuration
=============

Django Settings
---------------

Add the following to your ``settings.py`` to configure paystack-django:

Basic Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps
        'djpaystack',
    ]

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_your_secret_key',
        'PUBLIC_KEY': 'pk_test_your_public_key',
    }

Get your keys from `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

It's recommended to use environment variables for sensitive data:

.. code-block:: python

    import os
    from decouple import config

    PAYSTACK = {
        'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
        'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
    }

Create a ``.env`` file:

.. code-block:: bash

    PAYSTACK_SECRET_KEY=sk_test_your_secret_key
    PAYSTACK_PUBLIC_KEY=pk_test_your_public_key

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

All supported optional settings (shown with their defaults):

.. code-block:: python

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_your_secret_key',   # required
        'PUBLIC_KEY': 'pk_test_your_public_key',

        # HTTP client
        'BASE_URL': 'https://api.paystack.co',
        'TIMEOUT': 30,            # request timeout (seconds)
        'MAX_RETRIES': 3,         # retries for idempotent (GET) requests only
        'VERIFY_SSL': True,

        # Webhooks
        'WEBHOOK_SECRET': None,            # defaults to SECRET_KEY (see below)
        'WEBHOOK_SIGNATURE_REQUIRED': True,  # reject unsigned webhooks (fail closed)
        'ALLOWED_WEBHOOK_IPS': [],

        # Behaviour
        'CALLBACK_URL': None,
        'CURRENCY': 'NGN',
        'ENVIRONMENT': 'production',   # or 'test'
        'AUTO_VERIFY_TRANSACTIONS': True,
        'CACHE_TIMEOUT': 300,

        # Logging / integration
        'LOG_REQUESTS': False,
        'LOG_RESPONSES': False,
        'ENABLE_SIGNALS': True,
        'ENABLE_MODELS': True,
    }

Webhook signing secret
~~~~~~~~~~~~~~~~~~~~~~~~

Paystack signs webhook payloads with your account **secret key** — there is no
separate webhook secret. Accordingly:

- ``WEBHOOK_SECRET`` is optional and **defaults to ``SECRET_KEY``**.
- Set ``WEBHOOK_SECRET`` only to override the signing key.
- When no signing key can be resolved and ``WEBHOOK_SIGNATURE_REQUIRED`` is
  ``True`` (default), incoming webhooks are **rejected** (fail closed). For local
  development only, set ``WEBHOOK_SIGNATURE_REQUIRED = False`` to bypass.

.. note::

   Environment variables are the user's responsibility. The earlier
   ``python-decouple`` examples are illustrative; install ``python-decouple``
   (or use ``os.environ``) in your own project if you want that pattern — it is
   no longer a dependency of paystack-django.

Models Configuration
--------------------

By default, the package creates several models in the ``djpaystack`` app. Customize models if needed:

.. code-block:: python

    # In your settings.py
    DJPAYSTACK_TRANSACTION_MODEL = 'myapp.CustomTransaction'
    DJPAYSTACK_CUSTOMER_MODEL = 'myapp.CustomCustomer'

Database Setup
--------------

Run migrations to create the necessary tables:

.. code-block:: bash

    python manage.py migrate djpaystack

Webhook Configuration
---------------------

**In Django URLs:**

Add the webhook endpoint to your ``urls.py``:

.. code-block:: python

    from django.urls import path
    from djpaystack.webhooks.views import webhook

    urlpatterns = [
        path('api/webhooks/paystack/', webhook, name='paystack-webhook'),
    ]

**In Paystack Dashboard:**

1. Go to `Settings > API Keys & Webhooks <https://dashboard.paystack.com/settings/developer>`_
2. Add your webhook URL: ``https://yourdomain.com/api/webhooks/paystack/``
3. Enable webhook events you want to receive (recommended: charge.success, charge.failed)

**Webhook Secret:**

Store the webhook secret from the dashboard:

.. code-block:: python

    PAYSTACK = {
        # ... other settings
        'WEBHOOK_SECRET': 'whsec_your_webhook_secret_from_dashboard',
    }

Testing Configuration
---------------------

Use test keys for development:

.. code-block:: python

    if DEBUG:
        PAYSTACK = {
            'SECRET_KEY': 'sk_test_...',
            'PUBLIC_KEY': 'pk_test_...',
        }
    else:
        PAYSTACK = {
            'SECRET_KEY': 'sk_live_...',
            'PUBLIC_KEY': 'pk_live_...',
        }

Logging Configuration
---------------------

Configure logging to debug Paystack requests:

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'paystack_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'paystack.log',
            },
        },
        'loggers': {
            'djpaystack': {
                'handlers': ['paystack_file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

Celery Configuration (Optional)
-------------------------------

For async processing of webhooks:

.. code-block:: python

    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    
    PAYSTACK = {
        # ... other settings
        'USE_CELERY': True,
    }

Environment-Specific Configuration
-----------------------------------

**Development:**

.. code-block:: python

    # settings/development.py
    DEBUG = True
    PAYSTACK = {
        'SECRET_KEY': 'sk_test_dev_key',
        'PUBLIC_KEY': 'pk_test_dev_key',
    }

**Production:**

.. code-block:: python

    # settings/production.py
    DEBUG = False
    PAYSTACK = {
        'SECRET_KEY': 'sk_live_production_key',
        'PUBLIC_KEY': 'pk_live_production_key',
        'WEBHOOK_SECRET': 'whsec_production_secret',
    }

Configuration Reference
-----------------------

=========================== ============================================= ===============================================
Setting                     Purpose                                       Default Value
=========================== ============================================= ===============================================
``SECRET_KEY``              Paystack secret API key (required)            None
``PUBLIC_KEY``              Paystack public API key (required)            None
``WEBHOOK_SECRET``          Webhook verification secret                   None
``WEBHOOK_TIMEOUT``         Webhook request timeout in seconds             60
``API_TIMEOUT``             API request timeout in seconds                30
``API_RETRIES``             Number of retries for failed API requests     3
``LOG_REQUESTS``            Whether to log all API requests               True
``LOG_FILE``                Path to log file                              'paystack.log'
``BUSINESS_NAME``           Your business name for receipts               None
``BUSINESS_EMAIL``          Your business email                           None
=========================== ============================================= ===============================================

Validation
----------

The package validates your configuration on startup. Common errors:

**Missing SECRET_KEY:**

.. code-block:: text

    PaystackConfigurationError: PAYSTACK['SECRET_KEY'] is required

**Missing PUBLIC_KEY:**

.. code-block:: text

    PaystackConfigurationError: PAYSTACK['PUBLIC_KEY'] is required

Make sure both keys are set in your Django settings.
