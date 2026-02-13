import django.dispatch

# Transaction signals
paystack_payment_successful = django.dispatch.Signal()
paystack_payment_failed = django.dispatch.Signal()

# Subscription signals
paystack_subscription_created = django.dispatch.Signal()
paystack_subscription_cancelled = django.dispatch.Signal()

# Transfer signals
paystack_transfer_successful = django.dispatch.Signal()
paystack_transfer_failed = django.dispatch.Signal()

# Refund signals
paystack_refund_processed = django.dispatch.Signal()

# Dispute signals
paystack_dispute_created = django.dispatch.Signal()
paystack_dispute_resolved = django.dispatch.Signal()
