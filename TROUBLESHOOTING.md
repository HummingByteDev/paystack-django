# Troubleshooting Guide

## Common Issues

### Installation Issues

#### "pip: command not found"

**Solution:** Install or upgrade pip:

```bash
# macOS/Linux
python -m pip install --upgrade pip

# Windows
python -m pip install --upgrade pip
```

#### "ModuleNotFoundError: No module named 'djpaystack'"

**Solution:** Make sure the package is installed:

```bash
pip install paystack-django
pip list | grep paystack-django  # verify installation
```

#### "No module named 'django'"

**Solution:** Install Django:

```bash
pip install Django
```

#### "Conflicting requirements"

**Solution:** Check for version conflicts:

```bash
pip list
pip check  # Show dependency issues
```

---

### Configuration Issues

#### "PaystackConfigurationError: PAYSTACK['SECRET_KEY'] is required"

**Solution:** Add PAYSTACK configuration to settings:

```python
# settings.py
PAYSTACK = {
    'SECRET_KEY': 'sk_test_xxxx',
    'PUBLIC_KEY': 'pk_test_xxxx',
}
```

#### "Paystack keys not being loaded"

**Solution:** Check your environment setup:

```python
# settings.py
import os
from decouple import config  # Better: use decouple

# Check if settings are loaded
PAYSTACK = {
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY', default=''),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY', default=''),
}

# Debug: print the configuration
import sys
if 'runserver' in sys.argv:
    print(f"SECRET_KEY: {PAYSTACK.get('SECRET_KEY', 'NOT SET')}")
```

#### "ModuleNotFoundError: No module named 'decouple'"

**Solution:** Install python-decouple:

```bash
pip install python-decouple
```

---

### API Connection Issues

#### "PaystackNetworkError: Connection failed"

**Possible causes:**

- Internet connection is down
- Firewall blocking requests
- Paystack API is down

**Solutions:**

```python
# Check internet connection
import requests
try:
    response = requests.get('https://api.paystack.co', timeout=5)
    print("Connection OK")
except Exception as e:
    print(f"Connection error: {e}")

# Check if Paystack API is up
response = requests.get('https://status.paystack.com')
print(response.text)
```

#### "SSLError: certificate verify failed"

**Solution 1:** Update certificates:

```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# Or use certifi package
pip install --upgrade certifi
```

**Solution 2:** Disable SSL verification (NOT recommended):

```python
PAYSTACK = {
    'VERIFY_SSL': False,  # Only for development/testing
}
```

#### "Connection timeout"

**Solution:** Increase timeout:

```python
PAYSTACK = {
    'TIMEOUT': 60,  # Default is 30 seconds
}
```

#### "PaystackAuthenticationError: Invalid secret key"

**Possible causes:**

- Wrong secret key
- Using live key in test mode or vice versa
- Key expired

**Solutions:**

```python
# Check if you're using the correct key
SECRET_KEY = 'sk_test_xxxx'  # Test mode key
# or
SECRET_KEY = 'sk_live_xxxx'  # Production key

# Verify key format (should start with sk_)
# Regenerate key in Paystack dashboard if needed
```

---

### Transaction Issues

#### "Transaction initialization returns error"

**Check the response:**

```python
response = client.transaction.initialize(
    email='test@example.com',
    amount=50000,
    reference='test-123'
)

if not response['status']:
    print(f"Error: {response.get('message')}")
    print(f"Data: {response.get('data')}")
```

#### "Cannot verify transaction"

**Debug steps:**

```python
# 1. Check the reference is correct
reference = 'test-123'

# 2. Try to fetch transaction details
try:
    response = client.transaction.verify(reference=reference)
    print(f"Status: {response['status']}")
    print(f"Data: {response.get('data')}")
except Exception as e:
    print(f"Error: {e}")

# 3. List transactions to find the right one
list_response = client.transaction.list(page=1)
print(list_response['data'])
```

#### "Transaction reference already used"

**Solution:** Use unique references:

```python
import uuid

reference = f"order-{uuid.uuid4().hex[:12]}"
response = client.transaction.initialize(
    email='test@example.com',
    amount=50000,
    reference=reference
)
```

---

### Webhook Issues

#### "Webhook is not being triggered"

**Check list:**

1. **Webhook URL is configured:**
   - Go to Paystack Dashboard → Settings → API Keys & Webhooks
   - Check webhook URL is correct and uses HTTPS
   - Ensure URL is publicly accessible

2. **Webhook endpoint is receiving requests:**

   ```python
   # In your view
   import logging
   logger = logging.getLogger(__name__)

   def handle_webhook(request):
       logger.info(f"Webhook received: {request.method}")
       # ...
   ```

3. **Check webhook signature:**

   ```python
   from djpaystack.webhooks.handlers import verify_webhook_signature

   def handle_webhook(request):
       is_valid = verify_webhook_signature(
           body=request.body,
           signature_header=request.META.get('HTTP_X_PAYSTACK_SIGNATURE'),
           webhook_secret=settings.PAYSTACK['WEBHOOK_SECRET']
       )

       if not is_valid:
           logger.warning("Invalid webhook signature")
           return JsonResponse({'status': 'invalid'}, status=403)

       logger.info("Webhook verified successfully")
       return JsonResponse({'status': 'ok'})
   ```

#### "PaystackWebhookError: Invalid signature"

**Solution:** Verify webhook secret is correct:

```python
# Check in Paystack dashboard
PAYSTACK = {
    'WEBHOOK_SECRET': 'whsec_xxxxx',  # Must match dashboard
}
```

#### "Webhook endpoint returns 404"

**Solution:** Check URL configuration:

```python
# urls.py
from django.urls import path
from djpaystack.webhooks.views import handle_webhook

urlpatterns = [
    path('webhooks/paystack/', handle_webhook, name='paystack_webhook'),
]

# Then test the URL
# GET http://localhost:8000/webhooks/paystack/ should redirect to Paystack
```

#### "Webhook receiving requests but not processing"

**Debug:**

```python
import json
import logging

logger = logging.getLogger(__name__)

def handle_webhook(request):
    try:
        payload = json.loads(request.body)
        logger.info(f"Webhook payload: {payload}")

        event = payload.get('event')
        data = payload.get('data')

        logger.info(f"Event: {event}")

        if event == 'charge.success':
            logger.info(f"Payment successful: {data.get('reference')}")

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=400)
```

---

### Database Issues

#### "ProgrammingError: table 'djpaystack\_...' does not exist"

**Solution:** Run migrations:

```bash
python manage.py migrate djpaystack
```

Or if you don't want to create tables:

```python
PAYSTACK = {
    'ENABLE_MODELS': False,  # Disable database models
}
```

#### "django.db.ProgrammingError"

**Solutions:**

```bash
# Make fresh migrations
python manage.py makemigrations djpaystack
python manage.py migrate djpaystack --fake-initial

# Or reset (dangerous - only for development)
python manage.py migrate djpaystack zero
python manage.py migrate djpaystack
```

---

### Testing Issues

#### "Tests fail with missing dependencies"

**Solution:**

```bash
pip install -e ".[dev]"  # Install with test dependencies
pytest djpaystack/tests  # Run tests
```

#### "pytest: command not found"

**Solution:**

```bash
pip install pytest pytest-django
```

#### "DJANGO_SETTINGS_MODULE not set"

**Solution:**

```bash
export DJANGO_SETTINGS_MODULE=tests.settings
pytest

# Or in one command
DJANGO_SETTINGS_MODULE=tests.settings pytest
```

---

### Performance Issues

#### "Slow API requests"

**Solutions:**

```python
# 1. Increase timeout
PAYSTACK = {
    'TIMEOUT': 60,
}

# 2. Enable caching
PAYSTACK = {
    'CACHE_TIMEOUT': 300,  # Cache responses for 5 minutes
}

# 3. Use async requests (if available)
```

#### "Too many API calls"

**Solutions:**

```python
# 1. Cache responses
from django.core.cache import cache

def get_customer(customer_code):
    cached = cache.get(f'customer_{customer_code}')
    if cached:
        return cached

    customer = client.customer.fetch(customer_code)
    cache.set(f'customer_{customer_code}', customer, 300)  # 5 minutes
    return customer

# 2. Batch operations
transactions = client.transaction.list(per_page=100)
```

---

### Logging & Debugging

#### "Enable debug logging"

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('djpaystack')
logger.setLevel(logging.DEBUG)

# Or in settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'djpaystack': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Enable request/response logging
PAYSTACK = {
    'LOG_REQUESTS': True,
    'LOG_RESPONSES': True,
}
```

#### "Check API response"

```python
response = client.transaction.initialize(
    email='test@example.com',
    amount=50000,
    reference='test-123'
)

# Pretty print response
import json
print(json.dumps(response, indent=2))
```

---

### Deployment Issues

#### "Works locally but not in production"

**Check:**

1. Environment variables are set
2. Database is migrated
3. Static files are collected
4. ALLOWED_HOSTS includes production domain
5. HTTPS is enabled
6. Secrets are not in code
7. Webhook URL is correct

```python
# settings.py
import os

ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
]

PAYSTACK = {
    'SECRET_KEY': os.environ.get('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': os.environ.get('PAYSTACK_PUBLIC_KEY'),
}
```

#### "ALLOWED_HOST error for webhooks"

**Solution:**

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

#### "Webhook IP rejection"

**Solution:** Allow Paystack IPs:

```python
PAYSTACK = {
    'ALLOWED_WEBHOOK_IPS': [
        '200.0.0.0/8',  # Example - check Paystack docs for actual IPs
    ]
}
```

Or disable IP checking (less secure):

```python
PAYSTACK = {
    'ALLOWED_WEBHOOK_IPS': [],  # Allow all IPs
}
```

---

## Getting Help

1. **Check this guide** - Most issues are covered here
2. **Read the docs** - [README.md](README.md), [API_REFERENCE.md](API_REFERENCE.md)
3. **Search GitHub issues** - [Issues](https://github.com/HummingByteDev/paystack-django/issues)
4. **Create an issue** - Provide:
   - Python version
   - Django version
   - paystack-django version
   - Exact error message
   - Minimal code to reproduce

5. **Contact support** - security@hummingbyte.com

---

## Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "django|paystack|requests"

# Check for dependency issues
pip check

# View Paystack configuration
python manage.py shell
>>> from django.conf import settings
>>> settings.PAYSTACK

# Test API connection
python manage.py shell
>>> from djpaystack import PaystackClient
>>> client = PaystackClient()
>>> print("Connected successfully")
```

---

**Last Updated:** February 2026
