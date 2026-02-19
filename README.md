# paystack-django

A comprehensive Django integration for the **Paystack Payment Gateway**. This package provides a complete, production-ready solution for integrating Paystack payments into your Django applications.

[![PyPI version](https://badge.fury.io/py/paystack-django.svg)](https://badge.fury.io/py/paystack-django)
[![Django Versions](https://img.shields.io/badge/Django-3.2%2B-green)](https://www.djangoproject.com)
[![Python Versions](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Complete Paystack API Coverage** — 26 API modules covering every Paystack endpoint
- **Django Models** — Pre-built models for transactions, customers, plans, subscriptions, transfers, and webhook events
- **Webhook System** — Signature-verified webhook handling with IP whitelisting and event deduplication
- **Django Signals** — Signals for payment success/failure, subscriptions, transfers, refunds, and disputes
- **System Checks** — Django startup checks validate your Paystack configuration
- **Context Manager** — `PaystackClient` supports `with` statements for clean session management
- **Retry & Backoff** — Automatic retries with exponential back-off on transient failures
- **Type Hints** — Fully typed with `py.typed` marker for IDE and mypy support
- **Production Ready** — Secure defaults, lazy logging, Decimal-safe currency conversion

## Supported Services

| Category | API Modules |
|----------|------------|
| **Payments** | Transactions, Charge, Payment Requests, Pages |
| **Customers** | Customers, Direct Debit, Dedicated Accounts |
| **Recurring** | Plans, Subscriptions |
| **Payouts** | Transfers, Transfer Recipients, Transfer Control |
| **Commerce** | Products, Splits, Subaccounts |
| **Operations** | Refunds, Disputes, Settlements, Bulk Charges |
| **Other** | Verification, Terminal, Virtual Terminal, Apple Pay, Integration, Miscellaneous |

## Installation

```bash
pip install paystack-django
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
}
```

### 2. Run Migrations

```bash
python manage.py migrate djpaystack
```

### 3. Initialize a Transaction

```python
from djpaystack import PaystackClient

client = PaystackClient()

response = client.transactions.initialize(
    email='customer@example.com',
    amount=50000,  # Amount in kobo (500 NGN)
    reference='order-001',
)

authorization_url = response['data']['authorization_url']
# Redirect user to authorization_url
```

The client can also be used as a context manager:

```python
with PaystackClient() as client:
    response = client.transactions.verify(reference='order-001')
```

### 4. Verify Transaction

```python
response = client.transactions.verify(reference='order-001')

if response['data']['status'] == 'success':
    print("Payment successful!")
```

### 5. Set Up Webhooks

```python
# urls.py
from django.urls import path
from djpaystack.webhooks.views import handle_webhook

urlpatterns = [
    path('webhooks/paystack/', handle_webhook, name='paystack_webhook'),
]
```

Configure the webhook URL in your [Paystack Dashboard](https://dashboard.paystack.com/settings/developer).

## Usage Examples

### Customers

```python
client = PaystackClient()

# Create customer
response = client.customers.create(
    email='customer@example.com',
    first_name='John',
    last_name='Doe',
    phone='2348012345678',
)

# Fetch customer
response = client.customers.fetch(email_or_code='CUS_xxxxx')
```

### Subscriptions

```python
# Create a plan
response = client.plans.create(
    name='Monthly Pro',
    amount=500000,  # 5,000 NGN
    interval='monthly',
)
plan_code = response['data']['plan_code']

# Subscribe a customer
response = client.subscriptions.create(
    customer='CUS_xxxxx',
    plan=plan_code,
    authorization='AUTH_xxxxx',
)
```

### Transfers

```python
# Create transfer recipient
response = client.transfer_recipients.create(
    type='nuban',
    name='John Doe',
    account_number='0000000000',
    bank_code='058',
)
recipient_code = response['data']['recipient_code']

# Initiate transfer
response = client.transfers.initiate(
    source='balance',
    amount=50000,
    recipient=recipient_code,
    reason='Payout',
)
```

### Charge (Card, Bank Transfer, USSD, QR, EFT)

```python
# Charge with bank transfer
response = client.charge.create(
    email='customer@example.com',
    amount=50000,
    bank_transfer={'account_expires_at': '2025-12-31T23:59:59'},
)

# Charge with QR code (scan-to-pay)
response = client.charge.create(
    email='customer@example.com',
    amount=50000,
    qr={'provider': 'visa'},
)
```

### Refunds

```python
# Create refund
response = client.refunds.create(transaction='123456')

# Retry a stuck refund
response = client.refunds.retry(id='123456')
```

### Dedicated Virtual Accounts

```python
# Single-step assignment
response = client.dedicated_accounts.assign(
    email='customer@example.com',
    first_name='John',
    last_name='Doe',
    phone='+2348012345678',
    preferred_bank='wema-bank',
)
```

### Dynamic Transaction Splits

```python
response = client.transactions.initialize(
    email='customer@example.com',
    amount=100000,
    split={
        'type': 'percentage',
        'bearer_type': 'account',
        'subaccounts': [
            {'subaccount': 'ACCT_xxx', 'share': 30},
            {'subaccount': 'ACCT_yyy', 'share': 20},
        ],
    },
)
```

## Webhook Signals

Listen for payment events using Django signals:

```python
from django.dispatch import receiver
from djpaystack.signals import paystack_payment_successful, paystack_payment_failed

@receiver(paystack_payment_successful)
def on_payment_success(sender, transaction_data, **kwargs):
    reference = transaction_data['reference']
    # Fulfil the order

@receiver(paystack_payment_failed)
def on_payment_failed(sender, transaction_data, **kwargs):
    reference = transaction_data['reference']
    # Notify the customer
```

Available signals: `paystack_payment_successful`, `paystack_payment_failed`, `paystack_subscription_created`, `paystack_subscription_cancelled`, `paystack_transfer_successful`, `paystack_transfer_failed`, `paystack_refund_processed`, `paystack_dispute_created`, `paystack_dispute_resolved`.

## Configuration Reference

```python
PAYSTACK = {
    # Required
    'SECRET_KEY': 'sk_...',
    'PUBLIC_KEY': 'pk_...',

    # Webhook
    'WEBHOOK_SECRET': 'whsec_...',
    'ALLOWED_WEBHOOK_IPS': [],  # Empty = Paystack default IPs

    # API behaviour
    'BASE_URL': 'https://api.paystack.co',
    'TIMEOUT': 30,
    'MAX_RETRIES': 3,
    'VERIFY_SSL': True,
    'CURRENCY': 'NGN',
    'ENVIRONMENT': 'production',  # 'production' or 'test'

    # Features
    'AUTO_VERIFY_TRANSACTIONS': True,
    'ENABLE_SIGNALS': True,
    'ENABLE_MODELS': True,
    'CACHE_TIMEOUT': 300,
    'LOG_REQUESTS': False,
    'LOG_RESPONSES': False,
    'CALLBACK_URL': None,
}
```

## Django Models

```python
from djpaystack.models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackPlan,
    PaystackSubscription,
    PaystackTransfer,
    PaystackWebhookEvent,
)
```

## Error Handling

```python
from djpaystack.exceptions import (
    PaystackError,
    PaystackAPIError,
    PaystackValidationError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)

try:
    response = client.transactions.verify(reference='ref-123')
except PaystackAuthenticationError:
    print("Invalid API key")
except PaystackNetworkError:
    print("Network error — will be retried automatically")
except PaystackAPIError as e:
    print(f"API error: {e}")
```

## Django Compatibility

| paystack-django | Django 3.2 | 4.0 | 4.1 | 4.2 | 5.0 | 5.2 | 6.0 |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.1.x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

Python 3.8 – 3.14 supported.

## Testing

```bash
pip install -e ".[dev]"
pytest --cov=djpaystack
```

## Documentation

Full documentation is available at [paystack-django.readthedocs.io](https://paystack-django.readthedocs.io/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE).

## Links

- [Full Documentation](https://paystack-django.readthedocs.io/)
- [PyPI](https://pypi.org/project/paystack-django/)
- [GitHub](https://github.com/HummingByteDev/paystack-django)
- [Bug Tracker](https://github.com/HummingByteDev/paystack-django/issues)
- [Changelog](CHANGELOG.md)

---

**Made with ❤️ by [Humming Byte](https://hummingbyte.org)**
