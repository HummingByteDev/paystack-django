# Installation & Setup Guide for paystack-django

## System Requirements

- Python 3.8 or higher
- Django 3.2 or higher
- pip or pip3

## Step 1: Install the Package

### From PyPI (Recommended)

```bash
pip install paystack-django
```

### From Source (Development)

```bash
git clone https://github.com/HummingByteDev/paystack-django.git
cd django-paystack
pip install -e .
```

## Step 2: Add to Django Settings

Add `djpaystack` to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djpaystack',  # Add this
]
```

## Step 3: Configure Paystack Settings

Add Paystack configuration to your Django settings:

```python
# settings.py

PAYSTACK = {
    'SECRET_KEY': 'sk_live_your_secret_key',
    'PUBLIC_KEY': 'pk_live_your_public_key',
    'WEBHOOK_SECRET': 'whsec_your_webhook_secret',  # Optional but recommended
    'ENVIRONMENT': 'production',  # or 'test'
}
```

### Getting Your Keys

1. Create an account on [Paystack](https://paystack.com)
2. Go to Settings → API Keys & Webhooks
3. Copy your Secret Key (starts with `sk_`)
4. Copy your Public Key (starts with `pk_`)
5. Copy your Webhook Secret (starts with `whsec_`)

## Step 4: Secure Your Credentials

**Never hardcode secrets!** Use environment variables:

```bash
# .env file (use python-decouple to load)
PAYSTACK_SECRET_KEY=sk_live_xxx
PAYSTACK_PUBLIC_KEY=pk_live_xxx
PAYSTACK_WEBHOOK_SECRET=whsec_xxx
```

```python
# settings.py
from decouple import config

PAYSTACK = {
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
    'WEBHOOK_SECRET': config('PAYSTACK_WEBHOOK_SECRET'),
    'ENVIRONMENT': config('PAYSTACK_ENVIRONMENT', default='test'),
}
```

Install python-decouple if needed:

```bash
pip install python-decouple
```

## Step 5: Run Migrations (Optional)

If you want to use the provided Django models:

```bash
python manage.py migrate djpaystack
```

## Step 6: Configure Webhooks (Optional but Recommended)

Add webhook URL to your project:

```python
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/webhooks/paystack/', include('djpaystack.webhooks.urls')),
]
```

Then set the webhook URL in your Paystack dashboard:

- Go to Settings → API Keys & Webhooks
- Set Webhook URL to: `https://yourdomain.com/api/webhooks/paystack/`
- Make sure HTTPS is used for webhooks

## Complete Configuration Example

Here's a complete Django settings configuration:

```python
# settings.py

from decouple import config

# ...existing settings...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djpaystack',
]

# Paystack Configuration
PAYSTACK = {
    # Required
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),

    # Webhooks
    'WEBHOOK_SECRET': config('PAYSTACK_WEBHOOK_SECRET'),
    'CALLBACK_URL': config('PAYSTACK_CALLBACK_URL', default='https://yoursite.com/callback/'),

    # Environment
    'ENVIRONMENT': config('PAYSTACK_ENVIRONMENT', default='test'),
    'CURRENCY': 'NGN',

    # API Settings
    'BASE_URL': 'https://api.paystack.co',
    'TIMEOUT': 30,
    'MAX_RETRIES': 3,
    'VERIFY_SSL': True,

    # Features
    'AUTO_VERIFY_TRANSACTIONS': True,
    'CACHE_TIMEOUT': 300,
    'LOG_REQUESTS': False,
    'LOG_RESPONSES': False,
    'ENABLE_SIGNALS': True,
    'ENABLE_MODELS': True,
    'ALLOWED_WEBHOOK_IPS': [],
}
```

## Testing Your Setup

Create a test view to verify everything works:

```python
# views.py
from django.http import JsonResponse
from djpaystack import PaystackClient

def test_paystack(request):
    try:
        client = PaystackClient()
        # Try to initialize a test transaction
        response = client.transaction.initialize(
            email='test@example.com',
            amount=10000,  # 100 NGN
            reference='test-123'
        )
        return JsonResponse({'status': 'success', 'data': response})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
```

Then visit the view in your browser. If it returns a valid response, your setup is correct!

## Docker Setup

Here's a sample Dockerfile for your Django app with paystack-django:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
```

## Common Issues & Solutions

### Issue: "ImportError: No module named 'djpaystack'"

**Solution:** Make sure you've installed the package:

```bash
pip install paystack-django
```

### Issue: "PaystackConfigurationError: PAYSTACK['SECRET_KEY'] is required"

**Solution:** Add PAYSTACK configuration to settings.py:

```python
PAYSTACK = {
    'SECRET_KEY': 'your-secret-key',
    'PUBLIC_KEY': 'your-public-key',
}
```

### Issue: "ModuleNotFoundError: No module named 'requests'"

**Solution:** Install missing dependency:

```bash
pip install requests
```

### Issue: "DisallowedHost" error for webhooks

**Solution:** Add webhook domain to ALLOWED_HOSTS:

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Issue: SSL certificate verification error

**Solution:** Either fix your SSL certificate, or disable SSL verification (NOT recommended for production):

```python
PAYSTACK = {
    'VERIFY_SSL': False,  # Don't do this in production!
}
```

## Next Steps

1. Read the [README.md](README.md) for quick start examples
2. Check [API_REFERENCE.md](API_REFERENCE.md) for API documentation
3. Review the [examples](#examples) below
4. Set up webhooks for payment notifications

## Quick Example

```python
from djpaystack import PaystackClient

# Initialize client
client = PaystackClient()

# Create a transaction
response = client.transaction.initialize(
    email='user@example.com',
    amount=50000,  # 500 NGN in kobo
    reference='unique-ref-123'
)

# Redirect user to payment page
if response['status']:
    payment_url = response['data']['authorization_url']
    print(f"Send user to: {payment_url}")

# Later, verify the payment
verified = client.transaction.verify(reference='unique-ref-123')
if verified['status'] and verified['data']['status'] == 'success':
    print("Payment successful!")
```

## Getting Help

- 📚 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/HummingByteDev/paystack-django/issues)
- 📧 [Contact Support](mailto:contact@hummingbyte.com)
- 💬 [GitHub Discussions](https://github.com/HummingByteDev/paystack-django/discussions)

## Resources

- [Paystack Official Documentation](https://paystack.com/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)
