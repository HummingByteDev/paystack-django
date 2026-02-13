.. _quickstart:

Quick Start
===========

This guide will get you up and running with paystack-django in 5 minutes.

1. Basic Setup
--------------

First, add paystack-django to your Django apps in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # Add this
        'djpaystack',
    ]

2. Configuration
----------------

Add your Paystack credentials to your ``settings.py``:

.. code-block:: python

    PAYSTACK = {
        'SECRET_KEY': 'sk_test_your_secret_key_here',
        'PUBLIC_KEY': 'pk_test_your_public_key_here',
    }

Get your keys from the `Paystack Dashboard <https://dashboard.paystack.com/settings/developer>`_.

3. Create Your First Transaction
--------------------------------

Create a simple view to initialize a transaction:

.. code-block:: python

    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from djpaystack.api.transactions import Transaction

    @require_http_methods(["POST"])
    def initialize_payment(request):
        """Initialize a Paystack transaction"""
        
        transaction = Transaction()
        
        response = transaction.initialize(
            email=request.POST.get('email'),
            amount=int(request.POST.get('amount')),  # Amount in kobo
            reference=f"payment-{request.user.id}-{datetime.now().timestamp()}"
        )
        
        if response.get('status'):
            # Redirect user to Paystack payment page
            return JsonResponse({
                'authorization_url': response['data']['authorization_url'],
                'access_code': response['data']['access_code'],
                'reference': response['data']['reference']
            })
        
        return JsonResponse({'error': response.get('message')}, status=400)

4. Verify Payment
-----------------

After the user completes payment, verify the transaction:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    def verify_payment(request):
        """Verify a Paystack transaction"""
        reference = request.GET.get('reference')
        
        transaction = Transaction()
        response = transaction.verify(reference)
        
        if response.get('status'):
            payment_data = response['data']
            
            if payment_data['status'] == 'success':
                # Payment successful - update your models
                print(f"Payment verified: {payment_data['reference']}")
                return JsonResponse({'message': 'Payment successful'})
        
        return JsonResponse({'error': 'Payment verification failed'}, status=400)

5. Handle Webhooks
------------------

Set up webhook handling for real-time payment notifications. Add to your ``urls.py``:

.. code-block:: python

    from django.urls import path
    from djpaystack.webhooks.views import webhook

    urlpatterns = [
        # ... your other urls
        path('paystack/webhook/', webhook, name='paystack-webhook'),
    ]

Then, add your webhook URL to the Paystack Dashboard:
``https://yourdomain.com/paystack/webhook/``

6. What's Next?
---------------

- Read the :ref:`configuration` guide for more options
- Check out :ref:`transactions` for detailed examples
- Explore :ref:`api/index` for all available classes and methods
- See :ref:`webhooks` for advanced webhook configuration

Example Views
-------------

Here's a complete example for handling payments:

.. code-block:: python

    from django.shortcuts import render, redirect
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from djpaystack.api.transactions import Transaction
    from djpaystack.models import Transaction as TransactionModel
    import json

    @require_http_methods(["GET", "POST"])
    def payment_page(request):
        """Display payment form and handle initialization"""
        
        if request.method == 'POST':
            data = json.loads(request.body)
            
            transaction = Transaction()
            response = transaction.initialize(
                email=data['email'],
                amount=data['amount'],
                metadata={
                    'user_id': request.user.id,
                    'order_id': data.get('order_id')
                }
            )
            
            if response.get('status'):
                return JsonResponse(response['data'])
            return JsonResponse({'error': response.get('message')}, status=400)
        
        return render(request, 'payment.html')

    @require_http_methods(["GET"])
    def payment_callback(request):
        """Handle Paystack callback"""
        reference = request.GET.get('reference')
        
        if not reference:
            return redirect('payment_page')
        
        transaction = Transaction()
        response = transaction.verify(reference)
        
        if response['status'] and response['data']['status'] == 'success':
            # Update your transaction model
            TransactionModel.objects.create(
                reference=reference,
                amount=response['data']['amount'],
                customer_email=response['data']['customer']['email'],
                status='success'
            )
            return redirect('payment_success')
        
        return redirect('payment_failed')

Tips
----

1. **Always use HTTPS in production** - Paystack requires secure connections
2. **Verify payments server-side** - Never trust client-side verification
3. **Handle webhooks properly** - Webhooks are more reliable than redirects
4. **Store transaction data** - Keep records for auditing and reconciliation
5. **Test with test credentials** - Use test keys before going live

Congratulations! You've set up your first payment integration. For more advanced usage, check the :ref:`api/index`.
