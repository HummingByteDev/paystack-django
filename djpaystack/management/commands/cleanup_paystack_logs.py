
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from djpaystack.models import PaystackWebhookEvent, PaystackTransaction


class Command(BaseCommand):
    help = 'Clean up old Paystack logs and webhook events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Delete records older than this many days (default: 90)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--webhooks-only',
            action='store_true',
            help='Only clean webhook events',
        )
        parser.add_argument(
            '--failed-only',
            action='store_true',
            help='Only delete failed/abandoned transactions',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        webhooks_only = options['webhooks_only']
        failed_only = options['failed_only']

        cutoff_date = timezone.now() - timedelta(days=days)

        self.stdout.write(f"Cleaning up records older than {days} days")
        self.stdout.write(f"Cutoff date: {cutoff_date}")

        if dry_run:
            self.stdout.write(self.style.WARNING(
                'DRY RUN - No records will be deleted'))

        # Clean webhook events
        webhook_events = PaystackWebhookEvent.objects.filter(
            created_at__lt=cutoff_date,
            processed=True  # Only delete processed events
        )
        webhook_count = webhook_events.count()

        if webhook_count > 0:
            self.stdout.write(f"\nWebhook events to delete: {webhook_count}")
            if not dry_run:
                webhook_events.delete()
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Deleted {webhook_count} webhook events'))
        else:
            self.stdout.write("No webhook events to delete")

        # Clean transactions (if not webhooks-only)
        if not webhooks_only:
            transaction_query = PaystackTransaction.objects.filter(
                created_at__lt=cutoff_date
            )

            # Filter by status if failed-only
            if failed_only:
                transaction_query = transaction_query.filter(
                    status__in=['failed', 'abandoned']
                )

            transaction_count = transaction_query.count()

            if transaction_count > 0:
                self.stdout.write(
                    f"\nTransactions to delete: {transaction_count}")
                if not dry_run:
                    transaction_query.delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Deleted {transaction_count} transactions')
                    )
            else:
                self.stdout.write("No transactions to delete")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\nDRY RUN complete - no records were actually deleted')
            )
        else:
            self.stdout.write(self.style.SUCCESS('\n✓ Cleanup complete!'))
