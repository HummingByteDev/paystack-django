import django.dispatch

# Transaction signals
paystack_payment_successful = django.dispatch.Signal()

# Subscription signals
paystack_subscription_created = django.dispatch.Signal()
paystack_subscription_cancelled = django.dispatch.Signal()
paystack_subscription_not_renewing = django.dispatch.Signal()
paystack_subscription_expiring_cards = django.dispatch.Signal()

# Transfer signals
paystack_transfer_successful = django.dispatch.Signal()
paystack_transfer_failed = django.dispatch.Signal()
paystack_transfer_reversed = django.dispatch.Signal()

# Refund signals
paystack_refund_pending = django.dispatch.Signal()
paystack_refund_processing = django.dispatch.Signal()
paystack_refund_processed = django.dispatch.Signal()
paystack_refund_failed = django.dispatch.Signal()

# Dispute signals
paystack_dispute_created = django.dispatch.Signal()
paystack_dispute_remind = django.dispatch.Signal()
paystack_dispute_resolved = django.dispatch.Signal()

# Customer Identification signals
paystack_customeridentification_success = django.dispatch.Signal()
paystack_customeridentification_failed = django.dispatch.Signal()

# Dedicated Account signals
paystack_dedicatedaccount_assign_success = django.dispatch.Signal()
paystack_dedicatedaccount_assign_failed = django.dispatch.Signal()

# Invoice signals
paystack_invoice_created = django.dispatch.Signal()
paystack_invoice_updated = django.dispatch.Signal()
paystack_invoice_payment_failed = django.dispatch.Signal()

# Payment Request signals
paystack_paymentrequest_pending = django.dispatch.Signal()
paystack_paymentrequest_success = django.dispatch.Signal()
