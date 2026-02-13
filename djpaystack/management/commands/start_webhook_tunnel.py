
from django.core.management.base import BaseCommand
from django.conf import settings
from djpaystack.dev import NgrokTunnel
from djpaystack.settings import paystack_settings
import sys


class Command(BaseCommand):
    help = 'Start ngrok tunnel for local webhook development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Django server port (default: 8000)',
        )
        parser.add_argument(
            '--subdomain',
            type=str,
            help='Custom ngrok subdomain (requires paid plan)',
        )
        parser.add_argument(
            '--region',
            type=str,
            default='us',
            choices=['us', 'eu', 'ap', 'au', 'sa', 'jp', 'in'],
            help='Ngrok region (default: us)',
        )
        parser.add_argument(
            '--auth-token',
            type=str,
            help='Ngrok auth token',
        )

    def handle(self, *args, **options):
        port = options['port']
        subdomain = options['subdomain']
        region = options['region']
        auth_token = options.get('auth_token')

        self.stdout.write(self.style.SUCCESS('Starting ngrok tunnel for webhook development...'))
        self.stdout.write(f'Django server port: {port}')

        try:
            tunnel = NgrokTunnel(port=port, region=region)
            public_url = tunnel.start(subdomain=subdomain, auth_token=auth_token)

            webhook_url = tunnel.get_webhook_url()
            dashboard_url = tunnel.get_dashboard_url()

            self.stdout.write(self.style.SUCCESS('\n✓ Ngrok tunnel started successfully!\n'))
            self.stdout.write(self.style.SUCCESS('━' * 70))
            self.stdout.write(self.style.SUCCESS(f'\n📡 Public URL: {public_url}'))
            self.stdout.write(self.style.SUCCESS(f'🔗 Webhook URL: {webhook_url}'))
            self.stdout.write(self.style.SUCCESS(f'📊 Dashboard: {dashboard_url}'))
            self.stdout.write(self.style.SUCCESS('\n━' * 70))

            self.stdout.write(self.style.WARNING('\n⚙️  Next steps:\n'))
            self.stdout.write('1. Make sure your Django server is running:')
            self.stdout.write(f'   python manage.py runserver {port}')
            self.stdout.write('\n2. Add this webhook URL to your Paystack Dashboard:')
            self.stdout.write(f'   {webhook_url}')
            self.stdout.write('\n3. Copy your webhook secret from Paystack Dashboard')
            self.stdout.write('   and add it to your settings:\n')
            self.stdout.write("   PAYSTACK = {")
            self.stdout.write("       'WEBHOOK_SECRET': 'your_webhook_secret',")
            self.stdout.write("   }")

            self.stdout.write(self.style.SUCCESS('\n✨ Ready to receive webhooks!\n'))
            self.stdout.write('Press Ctrl+C to stop the tunnel...\n')

            # Keep the tunnel running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stdout.write('\n\nStopping tunnel...')
                tunnel.stop()
                self.stdout.write(self.style.SUCCESS('✓ Tunnel stopped'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            sys.exit(1)
