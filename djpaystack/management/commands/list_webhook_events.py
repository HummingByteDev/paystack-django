
from django.core.management.base import BaseCommand
from djpaystack.webhooks.events import WebhookEvent


class Command(BaseCommand):
    help = 'List all available Paystack webhook event types'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Available Paystack Webhook Events:\n'))
        self.stdout.write('━' * 70)

        events = {
            'Charge Events': [
                WebhookEvent.CHARGE_SUCCESS,
                WebhookEvent.CHARGE_FAILED,
            ],
            'Transfer Events': [
                WebhookEvent.TRANSFER_SUCCESS,
                WebhookEvent.TRANSFER_FAILED,
                WebhookEvent.TRANSFER_REVERSED,
            ],
            'Subscription Events': [
                WebhookEvent.SUBSCRIPTION_CREATE,
                WebhookEvent.SUBSCRIPTION_DISABLE,
                WebhookEvent.SUBSCRIPTION_NOT_RENEW,
                WebhookEvent.SUBSCRIPTION_EXPIRING_CARDS,
            ],
            'Invoice Events': [
                WebhookEvent.INVOICE_CREATE,
                WebhookEvent.INVOICE_UPDATE,
                WebhookEvent.INVOICE_PAYMENT_FAILED,
            ],
            'Customer Events': [
                WebhookEvent.CUSTOMERIDENTIFICATION_SUCCESS,
                WebhookEvent.CUSTOMERIDENTIFICATION_FAILED,
            ],
            'Refund Events': [
                WebhookEvent.REFUND_PENDING,
                WebhookEvent.REFUND_PROCESSED,
                WebhookEvent.REFUND_FAILED,
            ],
            'Dispute Events': [
                WebhookEvent.DISPUTE_CREATE,
                WebhookEvent.DISPUTE_REMIND,
                WebhookEvent.DISPUTE_RESOLVE,
            ],
            'Other Events': [
                WebhookEvent.DEDICATEDACCOUNT_ASSIGN_SUCCESS,
                WebhookEvent.DEDICATEDACCOUNT_ASSIGN_FAILED,
                WebhookEvent.PAYMENTREQUEST_PENDING,
                WebhookEvent.PAYMENTREQUEST_SUCCESS,
                WebhookEvent.PRODUCTORDER_PENDING,
                WebhookEvent.PRODUCTORDER_SUCCESS,
                WebhookEvent.TERMINAL_LIVE,
                WebhookEvent.TERMINAL_OFFLINE,
            ]
        }

        for category, event_list in events.items():
            self.stdout.write(f'\n{category}:')
            for event in event_list:
                self.stdout.write(f'  • {event.value}')

        self.stdout.write('\n' + '━' * 70)
        self.stdout.write('\nUsage:')
        self.stdout.write('  python manage.py test_webhook charge.success')
        self.stdout.write('  python manage.py test_webhook transfer.failed --amount 100000\n')
