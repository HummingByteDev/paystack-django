SECRET_KEY = 'test-secret-key-for-djpaystack-testing'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'djpaystack',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
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
