.. _troubleshooting:

Troubleshooting
===============

Common Issues and Solutions
---------------------------

**Import Error: No module named 'djpaystack'**

Solution: Install the package.

.. code-block:: bash

    pip install paystack-django

**PaystackConfigurationError**

Missing required configuration. Add to settings.py:

.. code-block:: python

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_...',
        'PUBLIC_KEY': 'pk_test_...',
    }

**Connection Errors**

Check your internet connection and Paystack API status. Verify API keys are correct.

**Webhook Verification Failed**

Ensure webhook secret is correct in settings and matches Paystack dashboard.

**Transaction Verification Returns 404**

Transaction might be pending. Wait a few seconds and try again.

**SSL Certificate Errors**

Update certificates or disable SSL verification in development only:

.. code-block:: python

    import urllib3
    urllib3.disable_warnings()

Need More Help?
---------------

- Check GitHub Issues: https://github.com/HummingByteDev/paystack-django/issues
- Read Paystack Docs: https://paystack.com/docs
- Join Discussions: https://github.com/HummingByteDev/paystack-django/discussions
