.. _installation:

Installation
============

Prerequisites
-------------

- Python 3.8 or higher
- Django 3.2 or higher
- pip or Poetry

Install from PyPI
-----------------

The recommended way to install paystack-django is using pip:

.. code-block:: bash

    pip install paystack-django

Install for Development
-----------------------

If you want to contribute or develop locally:

.. code-block:: bash

    git clone https://github.com/HummingByteDev/paystack-django.git
    cd django-paystack
    pip install -e ".[dev]"

Docker Installation
-------------------

If you're using Docker, add this to your requirements.txt:

.. code-block:: text

    paystack-django>=1.0.0
    Django>=3.2

Then install in your Dockerfile:

.. code-block:: dockerfile

    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

Verify Installation
-------------------

After installation, verify that the package is properly installed:

.. code-block:: bash

    python -c "import djpaystack; print(djpaystack.__version__)"

Troubleshooting
---------------

**ImportError: No module named 'djpaystack'**

Make sure you've installed the package:

.. code-block:: bash

    pip install paystack-django

**ModuleNotFoundError: No module named 'django'**

Install Django:

.. code-block:: bash

    pip install "Django>=3.2"

**SSL Certificate or Proxy Issues**

If you're behind a corporate proxy:

.. code-block:: bash

    pip install --proxy [user:passwd@]proxy.server:port paystack-django

Next Steps
----------

Once installed, proceed to :ref:`configuration` to set up your Django settings.
