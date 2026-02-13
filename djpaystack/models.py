"""
Django models for Paystack data
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaystackBaseModel(models.Model):
    """Base model for Paystack entities"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PaystackTransaction(PaystackBaseModel):
    """Model for storing Paystack transactions"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    reference = models.CharField(max_length=255, unique=True, db_index=True)
    amount = models.BigIntegerField(help_text=_("Amount in kobo"))
    currency = models.CharField(max_length=3, default='NGN')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)

    customer_email = models.EmailField()
    customer_code = models.CharField(max_length=255, null=True, blank=True)

    authorization_code = models.CharField(
        max_length=255, null=True, blank=True)
    authorization_url = models.URLField(null=True, blank=True)
    access_code = models.CharField(max_length=255, null=True, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    channel = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    fees = models.BigIntegerField(null=True, blank=True)
    fees_split = models.JSONField(null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
            models.Index(fields=['customer_email']),
        ]

    def __str__(self):
        return f"{self.reference} - {self.status}"


class PaystackCustomer(PaystackBaseModel):
    """Model for storing Paystack customers"""

    customer_code = models.CharField(
        max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    risk_action = models.CharField(max_length=20, default='default')

    metadata = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.customer_code})"


class PaystackWebhookEvent(PaystackBaseModel):
    """Model for storing webhook events"""

    event_type = models.CharField(max_length=100, db_index=True)
    event_id = models.CharField(max_length=255, unique=True, db_index=True)

    data = models.JSONField()
    processed = models.BooleanField(default=False, db_index=True)
    processing_error = models.TextField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'processed']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.event_id}"


class PaystackSubscription(PaystackBaseModel):
    """Model for storing Paystack subscriptions"""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('non-renewing', 'Non-Renewing'),
        ('attention', 'Attention'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    subscription_code = models.CharField(
        max_length=255, unique=True, db_index=True)
    customer_code = models.CharField(max_length=255, db_index=True)
    plan_code = models.CharField(max_length=255, db_index=True)

    amount = models.BigIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, db_index=True)

    next_payment_date = models.DateTimeField(null=True, blank=True)

    email_token = models.CharField(max_length=255, null=True, blank=True)
    authorization_code = models.CharField(
        max_length=255, null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subscription_code} - {self.status}"


class PaystackPlan(PaystackBaseModel):
    """Model for storing Paystack plans"""

    INTERVAL_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('biannually', 'Biannually'),
        ('annually', 'Annually'),
    ]

    plan_code = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES)

    description = models.TextField(null=True, blank=True)
    currency = models.CharField(max_length=3, default='NGN')

    send_invoices = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    metadata = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.plan_code})"


class PaystackTransfer(PaystackBaseModel):
    """Model for storing Paystack transfers"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('otp', 'OTP'),
        ('queued', 'Queued'),
    ]

    transfer_code = models.CharField(
        max_length=255, unique=True, db_index=True)
    reference = models.CharField(max_length=255, unique=True, db_index=True)

    amount = models.BigIntegerField()
    currency = models.CharField(max_length=3, default='NGN')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, db_index=True)

    recipient_code = models.CharField(max_length=255, db_index=True)
    reason = models.TextField(null=True, blank=True)

    transferred_at = models.DateTimeField(null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transfer_code} - {self.status}"
