.. _installation:

Installation
============

Prerequisites
-------------

- Python 3.8 or higher
- Django 3.2 or higher
- pip (or Poetry / PDM)

Install from PyPI
-----------------

.. code-block:: bash

    pip install paystack-django

With development extras:

.. code-block:: bash

    pip install paystack-django[dev]

Install for Development
-----------------------

.. code-block:: bash

    git clone https://github.com/HummingByteDev/paystack-django.git
    cd django-paystack
    pip install -e ".[dev]"

Docker
------

Add to your ``requirements.txt``:

.. code-block:: text

    paystack-django>=1.1.0

Verify Installation
-------------------

.. code-block:: bash

    python -c "import djpaystack; print(djpaystack.__version__)"
    # 1.1.0

Django Setup
------------

Add ``djpaystack`` to ``INSTALLED_APPS`` and run migrations:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'djpaystack',
    ]

.. code-block:: bash

    python manage.py migrate djpaystack

On startup, Django system checks will verify that ``PAYSTACK['SECRET_KEY']`` is configured
(error ``djpaystack.E001``) and warn if ``PAYSTACK['WEBHOOK_SECRET']`` is missing
(warning ``djpaystack.W001``).

Dependencies
------------

``paystack-django`` installs the following automatically:

- ``Django >= 3.2``
- ``requests >= 2.25.0``
- ``urllib3 >= 1.26.0``

No other dependencies are required. Configuration values are read from Django's
``settings.PAYSTACK`` dictionary — use ``os.environ``, ``django-environ``, or any
config loader of your choice.

Troubleshooting
---------------

**ImportError: No module named 'djpaystack'**

Ensure the package is installed in the correct virtual environment:

.. code-block:: bash

    pip install paystack-django

**SSL Certificate or Proxy Issues**

.. code-block:: bash

    pip install --proxy [user:passwd@]proxy.server:port paystack-django

Next Steps
----------

Once installed, proceed to :ref:`configuration` to set up your API keys.
