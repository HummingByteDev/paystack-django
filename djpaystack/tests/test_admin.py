
from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from djpaystack.admin import (
    PaystackTransactionAdmin,
    PaystackCustomerAdmin,
    PaystackWebhookEventAdmin,
    PaystackSubscriptionAdmin,
    PaystackPlanAdmin,
    PaystackTransferAdmin,
)
from djpaystack.models import (
    PaystackTransaction,
    PaystackCustomer,
    PaystackWebhookEvent,
    PaystackSubscription,
    PaystackPlan,
    PaystackTransfer,
)


class TestAdminRegistration(TestCase):
    """Test that admin classes are properly configured"""

    def setUp(self):
        self.site = AdminSite()

    def test_transaction_admin_list_display(self):
        admin = PaystackTransactionAdmin(PaystackTransaction, self.site)
        self.assertIn('reference', admin.list_display)
        self.assertIn('status', admin.list_display)
        self.assertIn('amount', admin.list_display)

    def test_transaction_admin_search_fields(self):
        admin = PaystackTransactionAdmin(PaystackTransaction, self.site)
        self.assertIn('reference', admin.search_fields)
        self.assertIn('customer_email', admin.search_fields)

    def test_transaction_admin_list_filter(self):
        admin = PaystackTransactionAdmin(PaystackTransaction, self.site)
        self.assertIn('status', admin.list_filter)
        self.assertIn('currency', admin.list_filter)

    def test_customer_admin_list_display(self):
        admin = PaystackCustomerAdmin(PaystackCustomer, self.site)
        self.assertIn('email', admin.list_display)
        self.assertIn('customer_code', admin.list_display)

    def test_webhook_event_admin_list_display(self):
        admin = PaystackWebhookEventAdmin(PaystackWebhookEvent, self.site)
        self.assertIn('event_type', admin.list_display)
        self.assertIn('processed', admin.list_display)

    def test_subscription_admin_list_display(self):
        admin = PaystackSubscriptionAdmin(PaystackSubscription, self.site)
        self.assertIn('subscription_code', admin.list_display)
        self.assertIn('status', admin.list_display)

    def test_plan_admin_list_display(self):
        admin = PaystackPlanAdmin(PaystackPlan, self.site)
        self.assertIn('name', admin.list_display)
        self.assertIn('plan_code', admin.list_display)

    def test_transfer_admin_list_display(self):
        admin = PaystackTransferAdmin(PaystackTransfer, self.site)
        self.assertIn('transfer_code', admin.list_display)
        self.assertIn('status', admin.list_display)

    def test_readonly_fields_include_timestamps(self):
        """Test all admins have created_at/updated_at as readonly"""
        admins = [
            (PaystackTransactionAdmin, PaystackTransaction),
            (PaystackCustomerAdmin, PaystackCustomer),
            (PaystackWebhookEventAdmin, PaystackWebhookEvent),
            (PaystackSubscriptionAdmin, PaystackSubscription),
            (PaystackPlanAdmin, PaystackPlan),
            (PaystackTransferAdmin, PaystackTransfer),
        ]
        for admin_cls, model_cls in admins:
            admin = admin_cls(model_cls, self.site)
            self.assertIn('created_at', admin.readonly_fields,
                          f"{admin_cls.__name__} missing created_at in readonly_fields")
            self.assertIn('updated_at', admin.readonly_fields,
                          f"{admin_cls.__name__} missing updated_at in readonly_fields")
