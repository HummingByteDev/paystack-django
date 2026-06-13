from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from djpaystack.client import PaystackClient
from djpaystack.models import PaystackCustomer, PaystackTransaction


class Command(BaseCommand):
    help = "Sync Paystack data to local database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--transactions",
            action="store_true",
            help="Sync transactions",
        )
        parser.add_argument(
            "--customers",
            action="store_true",
            help="Sync customers",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of days to sync (default: 30)",
        )

    def handle(self, *args, **options):
        client = PaystackClient()

        if options["transactions"]:
            self.stdout.write("Syncing transactions...")
            self.sync_transactions(client, options["days"])

        if options["customers"]:
            self.stdout.write("Syncing customers...")
            self.sync_customers(client, options["days"])

        self.stdout.write(self.style.SUCCESS("Sync completed successfully"))

    def sync_transactions(self, client, days):
        """Sync transactions from Paystack.

        honours ``--days`` (server-side date filter) and iterates
        lazily so memory stays bounded regardless of volume.
        """
        from_date = (timezone.now() - timedelta(days=days)).date().isoformat()

        synced = 0
        for txn in client.transactions.iter_all(from_date=from_date, per_page=100):
            PaystackTransaction.objects.update_or_create(
                reference=txn["reference"],
                defaults={
                    "amount": txn["amount"],
                    "currency": txn.get("currency", "NGN"),
                    "status": txn["status"],
                    "customer_email": txn.get("customer", {}).get("email"),
                    "raw_response": txn,
                },
            )
            synced += 1

        self.stdout.write(f"Synced {synced} transactions (last {days} days)")

    def sync_customers(self, client, days):
        """Sync customers from Paystack (lazy iteration)."""
        from_date = (timezone.now() - timedelta(days=days)).date().isoformat()

        synced = 0
        for cust in client.customers.iter_all(from_date=from_date, per_page=100):
            PaystackCustomer.objects.update_or_create(
                customer_code=cust["customer_code"],
                defaults={
                    "email": cust["email"],
                    "first_name": cust.get("first_name"),
                    "last_name": cust.get("last_name"),
                    "raw_response": cust,
                },
            )
            synced += 1

        self.stdout.write(f"Synced {synced} customers (last {days} days)")
