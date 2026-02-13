# Security Policy

## Reporting Security Issues

**Do not open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability in paystack-django, please email us at:
**dev@hummingbyte.org**

Please include:

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Your recommended fix (if you have one)

We will acknowledge receipt within 48 hours and work on a fix as soon as possible.

## Security Best Practices

### 1. API Keys & Secrets

**Never hardcode secrets in your code:**

```python
# ❌ BAD - Never do this!
PAYSTACK = {
    'SECRET_KEY': 'sk_live_xxx',
}
```

**Always use environment variables:**

```python
# ✅ GOOD - Use environment variables
from decouple import config

PAYSTACK = {
    'SECRET_KEY': config('PAYSTACK_SECRET_KEY'),
    'PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
}
```

**Store secrets securely:**

- Use `.env` files (add to `.gitignore`)
- Use environment variable services (AWS Secrets Manager, HashiCorp Vault, etc.)
- Use Django-Environ or python-decouple for loading
- Rotate keys regularly

### 2. Webhook Validation

**Always verify webhook signatures:**

```python
from djpaystack.webhooks.handlers import verify_webhook_signature

def handle_webhook(request):
    # Verify signature before processing
    is_valid = verify_webhook_signature(
        body=request.body,
        signature_header=request.META.get('HTTP_X_PAYSTACK_SIGNATURE'),
        webhook_secret=settings.PAYSTACK['WEBHOOK_SECRET']
    )

    if not is_valid:
        return JsonResponse({'status': 'invalid'}, status=403)

    # Process webhook
    payload = json.loads(request.body)
    # ...
```

### 3. HTTPS Only

**Always use HTTPS:**

```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

### 4. Allowed Webhook IPs

**Whitelist Paystack webhook IPs (if available):**

```python
PAYSTACK = {
    'ALLOWED_WEBHOOK_IPS': [
        '196.0.0.0/24',  # Example Paystack IP range
    ]
}
```

### 5. Input Validation

**Always validate user input:**

```python
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

try:
    validate_email(user_email)
except ValidationError:
    return JsonResponse({'error': 'Invalid email'}, status=400)
```

### 6. Cross-Site Request Forgery (CSRF)

**Ensure CSRF protection is enabled:**

```python
# settings.py
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
]

# In templates
{% csrf_token %}
```

### 7. SQL Injection Prevention

**Use Django ORM (always):**

```python
# ✅ GOOD - ORM prevents injection
customer = Customer.objects.filter(email=email_from_form)

# ❌ BAD - Raw SQL is vulnerable
Customer.objects.raw(f"SELECT * FROM customers WHERE email = '{email_from_form}'")
```

### 8. Cross-Site Scripting (XSS)

**Escape user input in templates:**

```django
{# ✅ GOOD - Django escapes by default #}
<p>{{ user_comment }}</p>

{# ❌ BAD - Disables escaping #}
<p>{{ user_comment|safe }}</p>
```

### 9. Rate Limiting

**Implement rate limiting on sensitive endpoints:**

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

@cache_page(60)  # Cache for 60 seconds
@require_http_methods(["POST"])
def create_payment(request):
    # ...
```

Or use a package like `django-ratelimit`:

```bash
pip install django-ratelimit
```

### 10. Logging

**Don't log sensitive information:**

```python
# ✅ GOOD
logger.info(f"Transaction {transaction_id} initialized")

# ❌ BAD - Logging secret key
logger.info(f"Using secret key: {PAYSTACK['SECRET_KEY']}")
```

### 11. Error Handling

**Don't expose sensitive errors:**

```python
# ✅ GOOD - Generic error message
except PaystackAPIError:
    return JsonResponse({'error': 'Payment processing failed'}, status=400)

# ❌ BAD - Exposes API details
except PaystackAPIError as e:
    return JsonResponse({'error': str(e)}, status=400)
```

### 12. Dependency Management

**Keep dependencies updated:**

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update dependencies safely
pip list --outdated
pip install --upgrade django requests
```

Or use Dependabot on GitHub.

### 13. Secret Rotation

**Periodically rotate keys:**

1. Generate new keys in Paystack dashboard
2. Add new keys as environment variables
3. Update your application to use new keys
4. Test thoroughly in staging
5. Deploy to production
6. Disable old keys in Paystack dashboard

### 14. Access Control

**Implement proper authorization:**

```python
from django.contrib.auth.decorators import login_required

@login_required
def payment_view(request):
    # Only authenticated users can access
    pass
```

### 15. Security Headers

**Add security headers:**

```python
# settings.py
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "cdn.example.com"),
    'style-src': ("'self'", "'unsafe-inline'"),
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## Regular Security Audits

Perform regular security audits:

```bash
# Check Python code
pip install bandit
bandit -r djpaystack

# OWASP Dependency-Check
pip install pip-audit
pip-audit

# Django security check
python manage.py check --deploy
```

## Compliance

### PCI-DSS Compliance

If handling card data:

- Never store full card numbers
- Use Paystack's hosted payment pages
- Use HTTPS everywhere
- Implement strong authentication
- Regularly monitor and test security

### GDPR Compliance

- Implement data retention policies
- Allow users to request data deletion
- Implement proper consent mechanisms
- Document data processing

## Version Support

We maintain security fixes for:

- **Latest version**: All bugs and security issues
- **Previous version**: Critical security issues only
- **Older versions**: No updates (users should upgrade)

## Security Changelog

See [CHANGELOG.md](CHANGELOG.md) for security updates in each release.

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
- [Paystack Security](https://paystack.com/docs/security/)

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities.

---

**Last Updated:** February 2024
**Version:** 1.0.0
