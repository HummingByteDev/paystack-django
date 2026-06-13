# paystack-django

A comprehensive Django integration for the **Paystack Payment Gateway**. This package provides a complete, production-ready solution for integrating Paystack payments into your Django applications.

[![PyPI version](https://badge.fury.io/py/paystack-django.svg)](https://badge.fury.io/py/paystack-django)
[![Django Versions](https://img.shields.io/badge/Django-4.2%2B-green)](https://www.djangoproject.com)
[![Python Versions](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **New in 2.0** — full coverage of the Paystack API (including Virtual Terminal,
> Direct Debit, Orders and Storefronts), memory-safe pagination with lazy
> `iter_all()` iterators, race-safe webhook deduplication, and a fail-closed
> webhook verification model. See the [CHANGELOG](CHANGELOG.md) for the full
> list, including **breaking changes**.

## Features

- **Full Paystack API Coverage** - Django-native clients for every Paystack API category
- **Django Models** - Pre-built models for transactions, customers, plans, subscriptions, transfers, and webhook events
- **Webhook Support** - Built-in webhook handling, HMAC-SHA512 signature verification (fails closed), and race-safe deduplication
- **Signal Support** - Django signals for payment, transfer, refund, subscription, and dispute events
- **Memory-safe Pagination** - Single-page `list()` plus lazy `iter_all()` iterators
- **Type Hints** - Typed public interface with a shipped `py.typed` marker
- **Comprehensive Documentation** - Detailed docs and examples

## Supported Services

The package provides Django-native clients for the following Paystack APIs.
"Full" means every endpoint in that category is implemented.

| Category | Status |
|---|---|
| Transactions | Full |
| Transaction Splits | Full |
| Customers (incl. authorization & direct-debit onboarding) | Full |
| Plans / Subscriptions | Full |
| Products | Full |
| Payment Pages / Payment Requests | Full |
| Transfers / Transfer Recipients / Transfer Control | Full |
| Refunds | Full |
| Disputes | Full |
| Subaccounts | Full |
| Dedicated Virtual Accounts | Full |
| Terminal | Full |
| Virtual Terminal | Full |
| Direct Debit | Full |
| Bulk Charges | Full |
| Charge | Full |
| Verification (Bank) | Full |
| Settlements | Full |
| Integration | Full |
| Apple Pay | Full |
| Orders | Full |
| Storefronts | Full |
| Miscellaneous (banks, countries, states) | Full |

> Some list endpoints currently support page-based pagination; cursor-based
> pagination is on the roadmap. See the parity matrix for per-endpoint detail.

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
    'ENVIRONMENT': 'production',  # or 'test'
}
```

> Paystack signs webhooks with your account **secret key**, so `WEBHOOK_SECRET`
> is optional and defaults to `SECRET_KEY`. Webhooks are **rejected** if no
> signing key can be resolved (fail closed).

### 2. Create PaystackClient Instance

```python
from djpaystack import PaystackClient

client = PaystackClient()

# Initialize a transaction
response = client.transactions.initialize(
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
verified = client.transactions.verify(reference='unique-reference-123')

if verified['data']['status'] == 'success':
    print("Payment successful!")
    # Update your database
else:
    print("Payment failed!")
```

### 4. Set Up Webhooks

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    # Exposes the webhook endpoint at /paystack/webhook/
    path('paystack/', include('djpaystack.webhooks.urls')),
]
```

Then set the webhook URL (e.g. `https://yoursite.com/paystack/webhook/`) in your
Paystack dashboard.

## Configuration

Complete configuration options available in `PAYSTACK` setting:

```python
PAYSTACK = {
    # Required
    'SECRET_KEY': 'your-secret-key',  # Required
    'PUBLIC_KEY': 'your-public-key',  # Required

    # Optional
    'BASE_URL': 'https://api.paystack.co',  # API base URL
    # Paystack signs webhooks with your SECRET_KEY. Leave WEBHOOK_SECRET unset
    # to use SECRET_KEY automatically; only set it to override.
    'WEBHOOK_SECRET': None,
    'WEBHOOK_SIGNATURE_REQUIRED': True,  # reject unsigned webhooks (fail closed)
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
response = client.transactions.initialize(
    email='user@example.com',
    amount=100000,
    reference='unique-ref-001',
    metadata={'order_id': 123}
)

# Verify transaction
response = client.transactions.verify(reference='unique-ref-001')

# List transactions (one page; use iter_all() to stream everything)
response = client.transactions.list(page=1, per_page=10)

# Fetch transaction
response = client.transactions.fetch(id_or_reference=123456)
```

### Customers

```python
# Create customer
response = client.customers.create(
    email='customer@example.com',
    first_name='John',
    last_name='Doe',
    phone='1234567890'
)

# List customers
response = client.customers.list(page=1, per_page=50)

# Fetch customer
response = client.customers.fetch(email_or_code='CUS_xxxxx')
```

### Subscriptions

```python
# Create subscription
response = client.subscriptions.create(
    customer='CUS_xxxxx',
    plan='PLN_xxxxx',
    authorization='AUTH_xxxxx'
)

# Enable subscription
response = client.subscriptions.enable(
    code='SUB_xxxxx',
    token='tok_xxxxx'
)

# Disable subscription
response = client.subscriptions.disable(code='SUB_xxxxx')
```

### Plans

```python
# Create plan
response = client.plans.create(
    name='Monthly Plan',
    amount=500000,  # 5000 NGN
    interval='monthly',
    description='Premium monthly subscription'
)

# List plans
response = client.plans.list(page=1)

# Fetch plan
response = client.plans.fetch(id_or_code='PLN_xxxxx')
```

### Transfers

```python
# Create transfer recipient
response = client.transfer_recipients.create(
    type='nuban',
    name='John Doe',
    account_number='0000000000',
    bank_code='001'
)

# Initiate transfer
response = client.transfers.initiate(
    source='balance',
    amount=50000,
    recipient='RCP_xxxxx',
    reference='transfer-001'
)

# Finalize transfer
response = client.transfers.finalize(transfer_code='TRF_xxxxx', otp='123456')
```

### Refunds

```python
# Create refund
response = client.refunds.create(
    transaction='123456'
)

# List refunds
response = client.refunds.list(page=1)

# Fetch refund
response = client.refunds.fetch(reference='123456')
```

### Orders, Storefronts & Virtual Terminal (new in 2.0)

```python
# Create a virtual terminal
client.virtual_terminal.create(
    name='In-store till',
    destinations=[{'target': '+2348000000000', 'name': 'Sales'}],
)

# Create a storefront and publish it
sf = client.storefront.create(name='My Shop', slug='my-shop', currency='NGN')
client.storefront.publish(sf['data']['id'])

# Customer direct-debit onboarding
init = client.customers.initialize_authorization(
    email='customer@example.com', channel='direct_debit',
)
client.customers.verify_authorization(init['data']['reference'])
```

## Database Models

The package includes Django models for persistence:

```python
from djpaystack.models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackPlan,
    PaystackSubscription,
    PaystackTransfer,
    PaystackWebhookEvent,
)

# Query transactions
transactions = PaystackTransaction.objects.filter(status='success')

# Transactions by customer
customer_transactions = PaystackTransaction.objects.filter(
    customer_email='user@example.com'
)

# Inspect stored webhook events
events = PaystackWebhookEvent.objects.filter(event_type='charge.success')
```

> Persistence is controlled by the `ENABLE_MODELS` setting (default `True`).
> Webhook handlers populate these models automatically.

## Webhooks

Handle Paystack webhooks automatically:

```python
# Webhook signals are dispatched automatically as events arrive
from django.dispatch import receiver

from djpaystack.signals import (
    paystack_payment_successful,
    paystack_payment_failed,
    paystack_transfer_successful,
    paystack_refund_processed,
    paystack_dispute_created,
)

@receiver(paystack_payment_successful)
def on_payment_success(sender, transaction_data, **kwargs):
    print(f"Payment successful: {transaction_data['reference']}")
    # Update your application

@receiver(paystack_payment_failed)
def on_payment_failed(sender, transaction_data, **kwargs):
    print(f"Payment failed: {transaction_data['reference']}")
    # Handle failed payment
```

Available signals: `paystack_payment_successful`, `paystack_payment_failed`,
`paystack_subscription_created`, `paystack_subscription_cancelled`,
`paystack_transfer_successful`, `paystack_transfer_failed`,
`paystack_refund_processed`, `paystack_dispute_created`,
`paystack_dispute_resolved`. Each receiver is called with a keyword argument
carrying the event payload (e.g. `transaction_data`, `transfer_data`,
`refund_data`, `dispute_data`).

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

The 2.x line is tested against the current and LTS Django releases:

| Package Version | Django 4.2 (LTS) | Django 5.2 (LTS) | Django 6.0 |
| --------------- | ---------------- | ---------------- | ---------- |
| 2.0.x           | ✅               | ✅               | ✅         |

## Python Compatibility

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

## Environment Variables

You can also configure using environment variables:

```bash
PAYSTACK_SECRET_KEY=sk_live_xxx
PAYSTACK_PUBLIC_KEY=pk_live_xxx
# Webhooks are signed with your secret key; use the same sk_... value here.
PAYSTACK_WEBHOOK_SECRET=sk_live_xxx
PAYSTACK_ENVIRONMENT=production
```

Load them however you prefer — for example with the standard library:

```python
import os

PAYSTACK = {
    'SECRET_KEY': os.environ['PAYSTACK_SECRET_KEY'],
    'PUBLIC_KEY': os.environ['PAYSTACK_PUBLIC_KEY'],
    'ENVIRONMENT': os.environ.get('PAYSTACK_ENVIRONMENT', 'test'),
}
```

> `python-decouple` is **not** a dependency of this package. If you prefer
> `decouple.config(...)`, install it in your own project.

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
    client.transactions.verify(reference='ref-123')
except PaystackAuthenticationError:
    print("Invalid API credentials")
except PaystackNetworkError:
    print("Network error occurred")
except PaystackAPIError as e:
    print(f"API error: {e}")
```

## Pagination

`list()` returns a **single page** (the first by default) and preserves
Paystack's `meta` block, so you control how much you fetch:

```python
response = client.transactions.list(
    page=1,
    per_page=50,
    from_date='2024-01-01',
    to_date='2024-12-31',
    status='success',
)

transactions = response['data']      # this page's records
meta = response['meta']              # {'page', 'pageCount', 'total', ...}
```

To stream **every** record across all pages without loading them all into
memory, use the lazy iterator:

```python
for txn in client.transactions.iter_all(status='success', from_date='2024-01-01'):
    process(txn)   # one record at a time; pages fetched on demand
```

> **Upgrading from 1.x?** Previously `list()` eagerly fetched *all* pages.
> It now returns one page — switch full scans to `iter_all()`. See the
> [CHANGELOG](CHANGELOG.md) for the full list of breaking changes.

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

Never hardcode secrets — load them from the environment:

```python
import os

PAYSTACK = {
    'SECRET_KEY': os.environ['PAYSTACK_SECRET_KEY'],
    'PUBLIC_KEY': os.environ['PAYSTACK_PUBLIC_KEY'],
}
```

### Webhook Verification

The built-in `PaystackWebhookView` verifies the HMAC-SHA512 signature on every
request and **rejects** anything it cannot verify (fail closed), so you normally
don't need to verify manually. If you handle webhooks yourself, use the helper:

```python
from djpaystack.utils import verify_webhook_signature

is_valid = verify_webhook_signature(
    request.body,                                      # payload (bytes)
    request.headers.get('X-Paystack-Signature', ''),   # signature
    settings.PAYSTACK['SECRET_KEY'],                   # secret (the signing key)
)

if not is_valid:
    return JsonResponse({'status': 'invalid'}, status=403)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Support

- 📚 [Full Documentation](https://paystack-django.readthedocs.io/)
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
