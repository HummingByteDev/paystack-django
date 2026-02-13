
from django.core.management.base import BaseCommand
from djpaystack.dev import WebhookTester
from djpaystack.settings import paystack_settings
from djpaystack.webhooks.events import WebhookEvent
import json


class Command(BaseCommand):
    help = 'Send test webhook events to local server'

    def add_arguments(self, parser):
        parser.add_argument(
            'event_type',
            type=str,
            help='Event type (e.g., charge.success, transfer.failed)',
        )
        parser.add_argument(
            '--url',
            type=str,
            default='http://localhost:8000/paystack/webhook/',
            help='Webhook URL (default: http://localhost:8000/paystack/webhook/)',
        )
        parser.add_argument(
            '--data',
            type=str,
            help='JSON data for the event',
        )
        parser.add_argument(
            '--reference',
            type=str,
            default='test_ref_123',
            help='Transaction reference',
        )
        parser.add_argument(
            '--amount',
            type=int,
            default=50000,
            help='Amount in kobo (default: 50000)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Customer email',
        )

    def handle(self, *args, **options):
        event_type = options['event_type']
        webhook_url = options['url']

        webhook_secret = paystack_settings.WEBHOOK_SECRET
        if not webhook_secret:
            self.stdout.write(self.style.ERROR(
                'WEBHOOK_SECRET not configured in settings'
            ))
            return

        self.stdout.write(f'Sending test webhook: {event_type}')
        self.stdout.write(f'Webhook URL: {webhook_url}')

        tester = WebhookTester(webhook_url, webhook_secret)

        try:
            # Use custom data if provided
            if options['data']:
                data = json.loads(options['data'])
                response = tester.send_event(event_type, data)

            # Or use convenience methods for common events
            elif event_type == WebhookEvent.CHARGE_SUCCESS:
                response = tester.send_charge_success(
                    reference=options['reference'],
                    amount=options['amount'],
                    email=options['email']
                )

            elif event_type == WebhookEvent.CHARGE_FAILED:
                response = tester.send_charge_failed(
                    reference=options['reference'],
                    amount=options['amount'],
                    email=options['email']
                )

            elif event_type == WebhookEvent.SUBSCRIPTION_CREATE:
                response = tester.send_subscription_create(
                    email=options['email']
                )

            elif event_type == WebhookEvent.TRANSFER_SUCCESS:
                response = tester.send_transfer_success(
                    amount=options['amount']
                )

            else:
                self.stdout.write(self.style.ERROR(
                    f'No convenience method for {event_type}. Use --data to provide custom data.'
                ))
                return

            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(
                    f'\n✓ Webhook sent successfully!'
                ))
                self.stdout.write(f'Response: {response.text}')
            else:
                self.stdout.write(self.style.ERROR(
                    f'\n✗ Webhook failed with status {response.status_code}'
                ))
                self.stdout.write(f'Response: {response.text}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
