SECRET_KEY = 'test-secret-key-for-djpaystack-testing'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'djpaystack',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PAYSTACK = {
    'SECRET_KEY': 'sk_test_xxxxxxxxxxxxx',
    'PUBLIC_KEY': 'pk_test_xxxxxxxxxxxxx',
    'WEBHOOK_SECRET': 'test_webhook_secret',
    'ENVIRONMENT': 'test',
    'ENABLE_MODELS': True,
    'ENABLE_SIGNALS': True,
}

USE_TZ = True
