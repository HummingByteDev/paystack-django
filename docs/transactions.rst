.. _transactions:

Transactions
============

The Transactions API is one of the most commonly used parts of paystack-django. Use it to initialize payments, verify transactions, and retrieve transaction details.

Overview
--------

A transaction represents a payment attempt in Paystack. Each transaction has:

- A unique reference
- An amount (in kobo, where 100 kobo = 1 naira)
- Customer email
- Authorization URL for payment
- Status (pending, success, failed, etc.)

Initializing a Transaction
---------------------------

Initialize a transaction to get the payment authorization URL:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    response = transaction.initialize(
        email='customer@example.com',
        amount=50000,  # 500 naira in kobo
        reference='unique-ref-123',
        metadata={
            'order_id': 12345,
            'user_id': 99,
        }
    )

    if response['status']:
        auth_url = response['data']['authorization_url']
        # Redirect user to auth_url

**Parameters:**

- ``email`` (str): Customer email address (required)
- ``amount`` (int): Amount in kobo (required, 100 kobo = 1 naira)
- ``reference`` (str): Unique transaction reference (optional, auto-generated if not provided)
- ``metadata`` (dict): Additional data to attach to transaction (optional)
- ``subaccount`` (str): For split payments (optional)
- ``currency`` (str): Transaction currency, default is 'NGN' (optional)
- ``plan`` (int): Subscription plan ID (optional, for subscriptions)

Verifying a Transaction
-----------------------

Verify that a transaction was successful:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    response = transaction.verify('unique-ref-123')

    if response['status'] and response['data']['status'] == 'success':
        # Transaction successful
        amount = response['data']['amount']  # in kobo
        reference = response['data']['reference']
        customer = response['data']['customer']
    else:
        # Transaction failed or pending
        status = response['data']['status']

**Response Data:**

.. code-block:: python

    {
        'id': 123456,
        'reference': 'unique-ref-123',
        'amount': 50000,  # in kobo
        'status': 'success',  # or 'pending', 'failed', 'abandoned'
        'customer': {
            'id': 789,
            'email': 'customer@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        },
        'authorization': {
            'authorization_code': 'AUTH_123xyz',
            'card_type': 'visa',
            'last4': '4321',
            'bin': '432100',
            'channel': 'card',
        },
        'paid_at': '2024-01-15T14:30:00.000Z',
        'message': 'Approved or successful'
    }

Listing Transactions
--------------------

Retrieve a list of transactions:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    
    # Get all transactions
    response = transaction.list()
    
    # With pagination
    response = transaction.list(page=1, per_page=50)
    
    # Filter by status
    response = transaction.list(status='success')
    
    # Filter by date
    response = transaction.list(
        start_date='2024-01-01',
        end_date='2024-01-31'
    )

Getting Transaction Details
----------------------------

Retrieve detailed information about a specific transaction:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    response = transaction.fetch(123456)  # Transaction ID

    if response['status']:
        transaction_data = response['data']
        print(f"Amount: {transaction_data['amount']}")
        print(f"Status: {transaction_data['status']}")

Charging Authorization
----------------------

If you have a saved authorization code, charge it again:

.. code-block:: python

    from djpaystack.api.transactions import Transaction

    transaction = Transaction()
    response = transaction.charge_authorization(
        authorization_code='AUTH_123xyz',
        email='customer@example.com',
        amount=50000,
        reference='recurring-charge-456'
    )

This is useful for subscription renewals or recurring charges.

Building Auth URL Manually
--------------------------

If you want to redirect users to Paystack without initializing first:

.. code-block:: python

    public_key = 'pk_test_...'
    reference = 'unique-ref-789'
    email = 'customer@example.com'
    amount = 50000  # in kobo

    auth_url = f"https://checkout.paystack.com/?key={public_key}" \
               f"&email={email}&amount={amount}&reference={reference}"

Complete Example
----------------

Here's a complete example view:

.. code-block:: python

    from django.shortcuts import render, redirect
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.contrib.auth.decorators import login_required
    from djpaystack.api.transactions import Transaction
    from djpaystack.models import Transaction as TransactionModel
    import uuid

    @login_required
    @require_http_methods(["GET", "POST"])
    def checkout(request):
        """Handle payment checkout"""
        
        if request.method == 'POST':
            amount = int(request.POST.get('amount'))
            email = request.POST.get('email')
            
            # Generate unique reference
            reference = f"payment-{request.user.id}-{uuid.uuid4()}"
            
            # Initialize transaction
            transaction = Transaction()
            response = transaction.initialize(
                email=email,
                amount=amount,
                reference=reference,
                metadata={
                    'user_id': request.user.id,
                    'username': request.user.username,
                }
            )
            
            if response.get('status'):
                # Save transaction record
                TransactionModel.objects.create(
                    reference=reference,
                    amount=amount,
                    customer_email=email,
                    status='pending',
                    user=request.user
                )
                
                # Redirect to payment page
                return redirect(response['data']['authorization_url'])
        
        return render(request, 'checkout.html')

    @require_http_methods(["GET"])
    def payment_callback(request):
        """Handle payment callback"""
        reference = request.GET.get('reference')
        
        if not reference:
            return redirect('checkout')
        
        # Verify transaction
        transaction = Transaction()
        response = transaction.verify(reference)
        
        if response.get('status') and response['data'].get('status') == 'success':
            # Update transaction record
            TransactionModel.objects.filter(
                reference=reference
            ).update(status='success')
            
            return render(request, 'payment_success.html', {
                'amount': response['data']['amount'],
                'reference': reference,
            })
        else:
            return render(request, 'payment_failed.html')

Error Handling
--------------

Always handle errors gracefully:

.. code-block:: python

    from djpaystack.api.transactions import Transaction
    from djpaystack.exceptions import PaystackError

    try:
        transaction = Transaction()
        response = transaction.initialize(
            email='customer@example.com',
            amount=50000,
        )
        
        if not response.get('status'):
            error_message = response.get('message', 'Unknown error')
            print(f"Transaction failed: {error_message}")
    
    except PaystackError as e:
        print(f"API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

Common Issues
-------------

**Transaction Verification Returns 404**

The transaction might be pending or the reference might be wrong. Wait a moment and verify again.

**Amount Format**

Amounts must be in kobo. To convert naira to kobo, multiply by 100:

.. code-block:: python

    amount_in_naira = 500
    amount_in_kobo = amount_in_naira * 100  # 50000
