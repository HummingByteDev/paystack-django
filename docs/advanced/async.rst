.. _advanced/async:

Async Support
=============

paystack-django supports async operations for high-performance applications.

Using Async
-----------

.. code-block:: python

    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from asgiref.sync import sync_to_async
    from djpaystack.api.transactions import Transaction

    @require_http_methods(["POST"])
    async def async_checkout(request):
        """Async payment initialization"""
        
        transaction = Transaction()
        
        # Make async API call
        response = await sync_to_async(transaction.initialize)(
            email=request.POST.get('email'),
            amount=int(request.POST.get('amount')),
        )
        
        return JsonResponse(response['data'])

With Celery
-----------

For background task processing:

.. code-block:: python

    from celery import shared_task
    from djpaystack.api.transactions import Transaction

    @shared_task
    def verify_transaction(reference):
        """Verify transaction in background"""
        transaction = Transaction()
        response = transaction.verify(reference)
        
        if response['status']:
            # Update your models
            pass
        
        return response

Configure Celery connection checking to avoid issues:

.. code-block:: python

    # settings.py
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'

Performance Tips
----------------

1. Use connection pooling for database
2. Cache Paystack responses when appropriate
3. Use async for I/O operations
4. Implement rate limiting for API calls
5. Monitor API quotas

.. code-block:: python

    from django.core.cache import cache

    def get_transaction_cached(reference):
        """Get transaction with caching"""
        cache_key = f'transaction_{reference}'
        
        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Fetch from API
        transaction = Transaction()
        response = transaction.verify(reference)
        
        # Cache for 5 minutes
        cache.set(cache_key, response, 300)
        
        return response
