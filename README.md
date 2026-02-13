# paystack-django

A comprehensive Django integration for the **Paystack Payment Gateway**. This package provides a complete, production-ready solution for integrating Paystack payments into your Django applications.

[![PyPI version](https://badge.fury.io/py/paystack-django.svg)](https://badge.fury.io/py/paystack-django)
[![Django Versions](https://img.shields.io/badge/Django-3.2%2B-green)](https://www.djangoproject.com)
[![Python Versions](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Complete Paystack API Integration** - Access all Paystack endpoints
- **Django Models** - Pre-built models for transactions, customers, plans, and more
- **Webhook Support** - Built-in webhook handling and verification
- **Signal Support** - Django signals for payment events
- **Async Ready** - Supports async operations
- **Type Hints** - Fully typed for better IDE support
- **Comprehensive Documentation** - Detailed docs and examples
- **Test Coverage** - Extensive test suite
- **Production Ready** - Used in production by multiple companies

## Supported Services

The package includes complete implementations for:

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
- **And many more...**

## Installation

Install using pip:

```bash
pip install paystack-django
```

Or install from source:

```bash
git clone https://github.com/HummingByteDev/paystack-django.git
cd django-paystack
pip install -e .
```

## Quick Start

### 1. Add to Django Settings

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'djpaystack',
]

PAYSTACK = {
    'SECRET_KEY': 'sk_live_your_secret_key_here',
    'PUBLIC_KEY': 'pk_live_your_public_key_here',
    'WEBHOOK_SECRET': 'whsec_your_webhook_secret',
    'ENVIRONMENT': 'production',  # or 'test'
}
```

### 2. Create PaystackClient Instance

```python
from djpaystack import PaystackClient

client = PaystackClient()

# Initialize a transaction
response = client.transaction.initialize(
    email='customer@example.com',
    amount=50000,  # in kobo (500 NGN)
    reference='unique-reference-123'
)

authorization_url = response['data']['authorization_url']
print(f"Redirect user to: {authorization_url}")
```

### 3. Verify Transaction

```python
# After user completes payment
verified = client.transaction.verify(reference='unique-reference-123')

if verified['data']['status'] == 'success':
    print("Payment successful!")
    # Update your database
else:
    print("Payment failed!")
```

### 4. Set Up Webhooks

```python
# urls.py
from django.urls import path
from djpaystack.webhooks import views as webhook_views

urlpatterns = [
    path('webhooks/paystack/', webhook_views.handle_webhook, name='paystack_webhook'),
]
```

Then configure the webhook URL in your Paystack dashboard.

## Configuration

Complete configuration options available in `PAYSTACK` setting:

```python
PAYSTACK = {
    # Required
    'SECRET_KEY': 'your-secret-key',  # Required
    'PUBLIC_KEY': 'your-public-key',  # Required

    # Optional
    'BASE_URL': 'https://api.paystack.co',  # API base URL
    'WEBHOOK_SECRET': 'your-webhook-secret',  # For webhook validation
    'CALLBACK_URL': 'https://yoursite.com/callback/',  # Callback URL
    'ENVIRONMENT': 'production',  # 'production' or 'test'
    'TIMEOUT': 30,  # Request timeout in seconds
    'MAX_RETRIES': 3,  # Number of retries
    'VERIFY_SSL': True,  # Verify SSL certificates
    'CURRENCY': 'NGN',  # Default currency
    'AUTO_VERIFY_TRANSACTIONS': True,  # Auto-verify on webhook
    'CACHE_TIMEOUT': 300,  # Cache timeout in seconds
    'LOG_REQUESTS': False,  # Log API requests
    'LOG_RESPONSES': False,  # Log API responses
    'ENABLE_SIGNALS': True,  # Enable Django signals
    'ENABLE_MODELS': True,  # Enable Django models
    'ALLOWED_WEBHOOK_IPS': [],  # Allowed webhook IPs (empty = all)
}
```

## Usage Examples

### Transactions

```python
from djpaystack import PaystackClient

client = PaystackClient()

# Initialize transaction
response = client.transaction.initialize(
    email='user@example.com',
    amount=100000,
    reference='unique-ref-001',
    metadata={'order_id': 123}
)

# Verify transaction
response = client.transaction.verify(reference='unique-ref-001')

# List transactions
response = client.transaction.list(page=1, per_page=10)

# Fetch transaction
response = client.transaction.fetch(id=123456)
```

### Customers

```python
# Create customer
response = client.customer.create(
    email='customer@example.com',
    first_name='John',
    last_name='Doe',
    phone='1234567890'
)

# List customers
response = client.customer.list(page=1, per_page=50)

# Fetch customer
response = client.customer.fetch(customer_code='CUS_xxxxx')
```

### Subscriptions

```python
# Create subscription
response = client.subscription.create(
    customer_code='CUS_xxxxx',
    plan_code='PLN_xxxxx',
    authorization_code='AUTH_xxxxx'
)

# Enable subscription
response = client.subscription.enable(
    code='SUB_xxxxx',
    token='tok_xxxxx'
)

# Disable subscription
response = client.subscription.disable(code='SUB_xxxxx')
```

### Plans

```python
# Create plan
response = client.plan.create(
    name='Monthly Plan',
    description='Premium monthly subscription',
    amount=500000,  # 5000 NGN
    interval='monthly',
    plan_code='PLN_custom'
)

# List plans
response = client.plan.list(page=1)

# Fetch plan
response = client.plan.fetch(plan_id=123)
```

### Transfers

```python
# Create transfer recipient
response = client.transfer_recipient.create(
    type='nuban',
    name='John Doe',
    account_number='0000000000',
    bank_code='001'
)

# Initiate transfer
response = client.transfer.initiate(
    source='balance',
    amount=50000,
    recipient='RCP_xxxxx',
    reference='transfer-001'
)

# Finalize transfer
response = client.transfer.finalize(transfer_code='TRF_xxxxx', otp='123456')
```

### Refunds

```python
# Create refund
response = client.refund.create(
    transaction='123456'
)

# List refunds
response = client.refund.list(page=1)

# Fetch refund
response = client.refund.fetch(refund_id='123')
```

## Database Models

The package includes Django models for persistence:

```python
from djpaystack.models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackPlan,
    PaystackProduct,
    PaystackRefund,
)

# Query transactions
transactions = PaystackTransaction.objects.filter(status='success')

# Transactions by customer
customer_transactions = PaystackTransaction.objects.filter(
    customer_email='user@example.com'
)

# Create a payment request
from djpaystack.models import PaymentRequest
request = PaymentRequest.objects.create(
    reference='req-001',
    amount=100000,
    description='Course enrollment'
)
```

## Webhooks

Handle Paystack webhooks automatically:

```python
# Webhook signals are automatically sent
from djpaystack.signals import transaction_verified, transaction_failed

from django.dispatch import receiver

@receiver(transaction_verified)
def on_payment_success(sender, transaction, **kwargs):
    print(f"Payment successful: {transaction.reference}")
    # Update your application

@receiver(transaction_failed)
def on_payment_failed(sender, transaction, **kwargs):
    print(f"Payment failed: {transaction.reference}")
    # Handle failed payment
```

## Testing

Run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

With coverage:

```bash
pytest --cov=djpaystack
```

Run tests across Python versions:

```bash
tox
```

## Django Compatibility

| Package Version | Django 3.2 | Django 4.0 | Django 4.1 | Django 4.2 | Django 5.0 | Django 5.2 | Django 6.0 |
| --------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| 1.0.x           | ✅         | ✅         | ✅         | ✅         | ✅         | ✅         | ✅         |

## Python Compatibility

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14

## Environment Variables

You can also configure using environment variables:

```bash
PAYSTACK_SECRET_KEY=sk_live_xxx
PAYSTACK_PUBLIC_KEY=pk_live_xxx
PAYSTACK_WEBHOOK_SECRET=whsec_xxx
PAYSTACK_ENVIRONMENT=production
```

Then use `python-decouple` to load them:

```python
from decouple import config

PAYSTACK = {
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
    'WEBHOOK_SECRET': config('PAYSTACK_WEBHOOK_SECRET'),
    'ENVIRONMENT': config('PAYSTACK_ENVIRONMENT', default='test'),
}
```

## Error Handling

The package provides specific exception classes:

```python
from djpaystack.exceptions import (
    PaystackError,
    PaystackAPIError,
    PaystackValidationError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)

try:
    client.transaction.verify(reference='ref-123')
except PaystackAuthenticationError:
    print("Invalid API credentials")
except PaystackNetworkError:
    print("Network error occurred")
except PaystackAPIError as e:
    print(f"API error: {e}")
```

## Pagination

List endpoints support pagination:

```python
response = client.transaction.list(
    page=1,
    per_page=50,
    from_date='2024-01-01',
    to_date='2024-12-31',
    customer=123,
    status='success'
)

# Access data
transactions = response['data']
pagination = response['meta']
```

## Logging

Enable logging to debug API interactions:

```python
import logging

# In settings.py
PAYSTACK = {
    'LOG_REQUESTS': True,
    'LOG_RESPONSES': True,
}

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('djpaystack')
```

## Security

### Environment Variables

Never hardcode secrets:

```python
import os
from decouple import config

PAYSTACK = {
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
    'WEBHOOK_SECRET': config('PAYSTACK_WEBHOOK_SECRET'),
}
```

### Webhook Verification

Verify all incoming webhooks:

```python
from djpaystack.webhooks.handlers import verify_webhook_signature

is_valid = verify_webhook_signature(
    body=request.body,
    signature_header=request.META.get('HTTP_X_PAYSTACK_SIGNATURE'),
    webhook_secret=PAYSTACK['WEBHOOK_SECRET']
)

if not is_valid:
    return JsonResponse({'status': 'invalid'}, status=403)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Support

- 📚 [Full Documentation](https://django-paystack.readthedocs.io)
- 🐛 [Report Issues](https://github.com/HummingByteDev/paystack-django/issues)
- 💬 [Discussions](https://github.com/HummingByteDev/paystack-django/discussions)
- 📧 [Email Support](mailto:dev@hummingbyte.org)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Paystack](https://paystack.com) for the excellent payment gateway
- Django community for the amazing framework
- All contributors and users of this package

## Disclaimer

This package is not affiliated with or endorsed by Paystack. It is maintained by Humming Byte as a community contribution.

---

**Made with ❤️ by [Humming Byte](https://hummingbyte.org)**
