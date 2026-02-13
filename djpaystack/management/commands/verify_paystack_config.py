
from django.core.management.base import BaseCommand
from djpaystack.client import PaystackClient
from djpaystack.settings import paystack_settings


class Command(BaseCommand):
    help = 'Verify Paystack configuration'

    def handle(self, *args, **options):
        self.stdout.write('Verifying Paystack configuration...\n')

        # Check settings
        self.stdout.write('Configuration:')
        self.stdout.write(f'  Base URL: {paystack_settings.BASE_URL}')
        self.stdout.write(f'  Currency: {paystack_settings.CURRENCY}')
        self.stdout.write(f'  Environment: {paystack_settings.ENVIRONMENT}')
        self.stdout.write(f'  Timeout: {paystack_settings.TIMEOUT}s')

        # Test API connection
        try:
            client = PaystackClient()
            response = client.miscellaneous.list_banks()

            if response.get('status'):
                self.stdout.write(self.style.SUCCESS(
                    '\n✓ API connection successful'))
                self.stdout.write(
                    f"  Found {len(response.get('data', []))} banks")
            else:
                self.stdout.write(self.style.ERROR(
                    '\n✗ API connection failed'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
