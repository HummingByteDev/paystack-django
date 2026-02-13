from django.contrib import admin
from .models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackWebhookEvent,
    PaystackSubscription,
    PaystackPlan,
    PaystackTransfer,
)


@admin.register(PaystackTransaction)
class PaystackTransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'customer_email',
                    'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['reference', 'customer_email', 'customer_code']
    readonly_fields = ['created_at', 'updated_at', 'raw_response']
    date_hierarchy = 'created_at'


@admin.register(PaystackCustomer)
class PaystackCustomerAdmin(admin.ModelAdmin):
    list_display = ['email', 'customer_code',
                    'first_name', 'last_name', 'created_at']
    search_fields = ['email', 'customer_code', 'first_name', 'last_name']
    readonly_fields = ['customer_code',
                       'created_at', 'updated_at', 'raw_response']
    date_hierarchy = 'created_at'


@admin.register(PaystackWebhookEvent)
class PaystackWebhookEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'event_id', 'processed', 'created_at']
    list_filter = ['event_type', 'processed', 'created_at']
    search_fields = ['event_type', 'event_id']
    readonly_fields = ['created_at', 'updated_at', 'data']
    date_hierarchy = 'created_at'


@admin.register(PaystackSubscription)
class PaystackSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscription_code', 'customer_code',
                    'plan_code', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['subscription_code', 'customer_code', 'plan_code']
    readonly_fields = ['subscription_code',
                       'created_at', 'updated_at', 'raw_response']
    date_hierarchy = 'created_at'


@admin.register(PaystackPlan)
class PaystackPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_code', 'amount',
                    'interval', 'currency', 'is_active', 'created_at']
    list_filter = ['interval', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'plan_code']
    readonly_fields = ['plan_code', 'created_at', 'updated_at', 'raw_response']


@admin.register(PaystackTransfer)
class PaystackTransferAdmin(admin.ModelAdmin):
    list_display = ['transfer_code', 'reference',
                    'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['transfer_code', 'reference', 'recipient_code']
    readonly_fields = ['transfer_code',
                       'created_at', 'updated_at', 'raw_response']
    date_hierarchy = 'created_at'
