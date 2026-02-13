# paystack-django API Documentation

## Quick Reference

### Base Client

```python
from djpaystack import PaystackClient

client = PaystackClient()
```

## Transaction Endpoints

### Initialize Transaction

```python
response = client.transaction.initialize(
    email='customer@example.com',
    amount=50000,  # in kobo
    reference='unique-reference',
    plan=None,
    invoice_limit=None,
    metadata=None,
    subaccount=None,
    currency=None,
    split=None,
    bearer=None
)
```

### Verify Transaction

```python
response = client.transaction.verify(reference='unique-reference')
# or
response = client.transaction.verify(id=123456)
```

### List Transactions

```python
response = client.transaction.list(
    page=1,
    per_page=50,
    customer=None,
    status=None,
    from_date=None,
    to_date=None
)
```

### Fetch Single Transaction

```python
response = client.transaction.fetch(id=123456)
```

### Timeline

```python
response = client.transaction.timeline(
    reference='unique-reference',
    id_type='reference'  # or 'id'
)
```

### Totals

```python
response = client.transaction.totals()
```

### Export

```python
response = client.transaction.export(
    filename=None,
    path=None
)
```

---

## Customer Endpoints

### Create Customer

```python
response = client.customer.create(
    email='customer@example.com',
    first_name=None,
    last_name=None,
    phone=None
)
```

### List Customers

```python
response = client.customer.list(
    page=1,
    per_page=50
)
```

### Fetch Customer

```python
response = client.customer.fetch(customer_code='CUS_xxxxx')
# or
response = client.customer.fetch(id=123)
```

### Update Customer

```python
response = client.customer.update(
    code='CUS_xxxxx',
    first_name=None,
    last_name=None,
    email=None,
    phone=None
)
```

### Whitelist/Blacklist

```python
response = client.customer.whitelist(
    action='whitelist',  # or 'blacklist'
    customer_code='CUS_xxxxx'
)
```

---

## Plan Endpoints

### Create Plan

```python
response = client.plan.create(
    name='Monthly Subscription',
    description=None,
    amount=500000,  # in kobo
    interval='monthly',  # daily, weekly, monthly, quarterly, half-yearly, yearly
    send_invoices=None,
    send_sms=None,
    hosted_invoice_url=None,
    invoice_limit=None,
    plan_code=None
)
```

### List Plans

```python
response = client.plan.list(
    page=1,
    per_page=50,
    interval=None,
    amount=None
)
```

### Fetch Plan

```python
response = client.plan.fetch(plan_id=123)
```

### Update Plan

```python
response = client.plan.update(
    id=123,
    name=None,
    description=None,
    amount=None,
    interval=None,
    send_invoices=None,
    send_sms=None,
    hosted_invoice_url=None,
    invoice_limit=None
)
```

---

## Subscription Endpoints

### Create Subscription

```python
response = client.subscription.create(
    customer_code='CUS_xxxxx',
    plan_code='PLN_xxxxx',
    authorization_code='AUTH_xxxxx',
    start_date=None
)
```

### List Subscriptions

```python
response = client.subscription.list(
    page=1,
    per_page=50,
    customer=None,
    plan=None
)
```

### Fetch Subscription

```python
response = client.subscription.fetch(code='SUB_xxxxx')
```

### Enable Subscription

```python
response = client.subscription.enable(
    code='SUB_xxxxx',
    token='tok_xxxxx'
)
```

### Disable Subscription

```python
response = client.subscription.disable(code='SUB_xxxxx')
```

---

## Transfer Recipient Endpoints

### Create Recipient

```python
response = client.transfer_recipient.create(
    type='nuban',  # or 'mobile_money', 'ghipss'
    name='John Doe',
    account_number='0000000000',
    bank_code='001',
    currency=None,
    authorization_key=None
)
```

### List Recipients

```python
response = client.transfer_recipient.list(
    page=1,
    per_page=50,
    type=None
)
```

### Fetch Recipient

```python
response = client.transfer_recipient.fetch(recipient_code='RCP_xxxxx')
```

### Update Recipient

```python
response = client.transfer_recipient.update(
    recipient_code='RCP_xxxxx',
    name=None,
    email=None,
    description=None
)
```

### Delete Recipient

```python
response = client.transfer_recipient.delete(recipient_code='RCP_xxxxx')
```

---

## Transfer Endpoints

### Initiate Transfer

```python
response = client.transfer.initiate(
    source='balance',
    amount=50000,
    recipient='RCP_xxxxx',
    reference='transfer-ref-001',
    reason=None,
    currency=None
)
```

### Finalize Transfer

```python
response = client.transfer.finalize(
    transfer_code='TRF_xxxxx',
    otp='123456'
)
```

### List Transfers

```python
response = client.transfer.list(
    page=1,
    per_page=50,
    customer=None,
    status=None
)
```

### Fetch Transfer

```python
response = client.transfer.fetch(transfer_code='TRF_xxxxx')
```

### Verify Transfer

```python
response = client.transfer.verify(reference='transfer-ref-001')
```

---

## Refund Endpoints

### Create Refund

```python
response = client.refund.create(
    transaction=123456,
    amount=None,
    currency=None,
    customer_note=None,
    merchant_note=None
)
```

### List Refunds

```python
response = client.refund.list(
    page=1,
    per_page=50,
    reference=None,
    currency=None
)
```

### Fetch Refund

```python
response = client.refund.fetch(refund_id=123)
```

---

## Verification Endpoints

### Verify Bank Account

```python
response = client.verification.verify_account(
    account_number='0000000000',
    bank_code='001'
)
```

### Verify BVN

```python
response = client.verification.bvn(bvn='12345678901')
```

### Get Banks

```python
response = client.verification.get_banks(
    country=None,
    use_cursor=None
)
```

---

## Response Format

All endpoints return a dictionary:

```python
{
    'status': True,  # or False
    'message': 'Authorization URL generated',
    'data': {
        # Endpoint-specific data
    }
}
```

### Error Handling

```python
from djpaystack.exceptions import (
    PaystackError,
    PaystackAPIError,
    PaystackValidationError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)

try:
    response = client.transaction.verify(reference='ref-123')
except PaystackAuthenticationError:
    print('Invalid credentials')
except PaystackNetworkError:
    print('Network error')
except PaystackAPIError as e:
    print(f'API Error: {e}')
```

---

## Configuration Reference

```python
PAYSTACK = {
    # Required
    'SECRET_KEY': 'sk_...',
    'PUBLIC_KEY': 'pk_...',

    # Optional - API
    'BASE_URL': 'https://api.paystack.co',
    'TIMEOUT': 30,
    'MAX_RETRIES': 3,
    'VERIFY_SSL': True,

    # Optional - Webhooks
    'WEBHOOK_SECRET': 'whsec_...',
    'CALLBACK_URL': 'https://yoursite.com/callback/',
    'ALLOWED_WEBHOOK_IPS': [],

    # Optional - Environment
    'ENVIRONMENT': 'production',  # or 'test'
    'CURRENCY': 'NGN',

    # Optional - Features
    'AUTO_VERIFY_TRANSACTIONS': True,
    'CACHE_TIMEOUT': 300,
    'LOG_REQUESTS': False,
    'LOG_RESPONSES': False,
    'ENABLE_SIGNALS': True,
    'ENABLE_MODELS': True,
}
```

---

## Examples

### Complete Payment Flow

```python
from djpaystack import PaystackClient

client = PaystackClient()

# 1. Initialize transaction
init_response = client.transaction.initialize(
    email='customer@example.com',
    amount=100000,  # 1000 NGN
    reference='order-12345'
)

if init_response['status']:
    auth_url = init_response['data']['authorization_url']
    print(f"Redirect user to: {auth_url}")

# 2. After payment, verify transaction
verify_response = client.transaction.verify(reference='order-12345')

if verify_response['status'] and verify_response['data']['status'] == 'success':
    print("Payment successful!")
    amount = verify_response['data']['amount'] / 100
    print(f"Amount paid: {amount} NGN")
else:
    print("Payment failed!")
```

### Create Recurring Payment

```python
# 1. Create customer
customer = client.customer.create(
    email='recurring@example.com',
    first_name='John'
)

# 2. Create plan
plan = client.plan.create(
    name='Monthly Subscription',
    amount=10000,  # 100 NGN
    interval='monthly',
    plan_code='PLAN_MONTHLY'
)

# 3. Initialize transaction to get authorization
init = client.transaction.initialize(
    email='recurring@example.com',
    amount=10000,
    reference='initial-transaction'
)

# User completes payment and returns

# 4. Get authorization
transaction = client.transaction.verify(reference='initial-transaction')
authorization = transaction['data']['authorization']

# 5. Create subscription
subscription = client.subscription.create(
    customer_code=customer['data']['customer_code'],
    plan_code='PLAN_MONTHLY',
    authorization_code=authorization['authorization_code']
)
```

---

For complete API documentation, visit [Paystack API Docs](https://paystack.com/docs/api)
