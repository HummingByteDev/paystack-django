"""
Management command to send simulated Paystack webhook events to a local server.

Usage:
    python manage.py paystack_webhook_event charge.success
    python manage.py paystack_webhook_event transfer.failed --amount 100000
    python manage.py paystack_webhook_event charge.success --data '{"reference": "ref_123"}'
    python manage.py paystack_webhook_event --list
"""

import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError

from djpaystack.settings import paystack_settings
from djpaystack.webhooks.events import WebhookEvent


# ------------------------------------------------------------------ #
# Sample data factories
# ------------------------------------------------------------------ #

def _base_customer(email: str) -> Dict[str, Any]:
    return {
        "id": 123456,
        "email": email,
        "customer_code": f"CUS_{uuid.uuid4().hex[:10].upper()}",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+2348012345678",
    }


def _make_charge_data(
    reference: str, amount: int, email: str, status: str = "success"
) -> Dict[str, Any]:
    return {
        "id": 987654,
        "reference": reference,
        "amount": amount,
        "currency": "NGN",
        "status": status,
        "channel": "card",
        "fees": int(amount * 0.015),
        "paid_at": datetime.now(timezone.utc).isoformat(),
        "customer": _base_customer(email),
        "authorization": {
            "authorization_code": f"AUTH_{uuid.uuid4().hex[:10].upper()}",
            "bin": "408408",
            "last4": "4081",
            "exp_month": "12",
            "exp_year": "2030",
            "channel": "card",
            "card_type": "visa",
            "bank": "TEST BANK",
            "brand": "visa",
            "reusable": True,
        },
        "metadata": {},
    }


def _make_transfer_data(
    amount: int, status: str = "success"
) -> Dict[str, Any]:
    return {
        "id": 456789,
        "transfer_code": f"TRF_{uuid.uuid4().hex[:10].upper()}",
        "amount": amount,
        "currency": "NGN",
        "status": status,
        "reference": f"trf_{uuid.uuid4().hex[:10]}",
        "recipient": {
            "recipient_code": f"RCP_{uuid.uuid4().hex[:10].upper()}",
            "type": "nuban",
            "name": "Test Recipient",
            "details": {"bank_code": "058", "account_number": "0000000000"},
        },
        "reason": "Test transfer",
    }


def _make_subscription_data(email: str) -> Dict[str, Any]:
    return {
        "id": 111222,
        "subscription_code": f"SUB_{uuid.uuid4().hex[:10].upper()}",
        "plan": {
            "plan_code": f"PLN_{uuid.uuid4().hex[:10].upper()}",
            "name": "Monthly Pro",
            "amount": 500000,
            "interval": "monthly",
        },
        "customer": _base_customer(email),
        "status": "active",
        "next_payment_date": "2026-03-21T00:00:00.000Z",
    }


def _make_refund_data(amount: int) -> Dict[str, Any]:
    return {
        "id": 334455,
        "transaction": 987654,
        "amount": amount,
        "currency": "NGN",
        "status": "processed",
        "refunded_at": datetime.now(timezone.utc).isoformat(),
        "customer_note": "Test refund",
        "merchant_note": "",
    }


def _make_dispute_data(amount: int) -> Dict[str, Any]:
    return {
        "id": 556677,
        "status": "awaiting-merchant-feedback",
        "amount": amount,
        "currency": "NGN",
        "transaction": {
            "id": 987654,
            "reference": f"txn_{uuid.uuid4().hex[:10]}",
            "amount": amount,
        },
        "category": "general",
        "resolution": None,
        "message": "Test dispute",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _make_customeridentification_data(
    email: str, status: str = "success"
) -> Dict[str, Any]:
    return {
        "customer_id": 123456,
        "customer_code": f"CUS_{uuid.uuid4().hex[:10].upper()}",
        "email": email,
        "identification": {
            "country": "NG",
            "type": "bvn",
            "value": "22012345678",
        },
        "reason": "" if status == "success" else "Could not verify identity",
    }


def _make_dedicatedaccount_data(
    email: str, status: str = "success"
) -> Dict[str, Any]:
    return {
        "customer": _base_customer(email),
        "dedicated_account": {
            "account_name": "PAYSTACK-Test User",
            "account_number": "0000000000",
            "bank": {"name": "Wema Bank", "id": 20, "slug": "wema-bank"},
            "id": 55555,
            "assignment": {"assignee_id": 100, "assignee_type": "Integration"},
        },
        "identification": {"country": "NG", "type": "bvn", "value": "22012345678"},
    }


def _make_invoice_data(
    email: str, amount: int, status: str = "success"
) -> Dict[str, Any]:
    return {
        "id": 667788,
        "invoice_code": f"INV_{uuid.uuid4().hex[:10].upper()}",
        "reference": f"inv_{uuid.uuid4().hex[:10]}",
        "domain": "test",
        "amount": amount,
        "currency": "NGN",
        "status": "payment-failed" if status == "failed" else status,
        "paid": status == "success",
        "customer": _base_customer(email),
        "description": "Monthly subscription",
        "due_date": "2026-03-15T00:00:00.000Z",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _make_paymentrequest_data(
    email: str, amount: int, status: str = "pending"
) -> Dict[str, Any]:
    return {
        "id": 889900,
        "request_code": f"PRQ_{uuid.uuid4().hex[:10].upper()}",
        "amount": amount,
        "currency": "NGN",
        "status": status,
        "customer": _base_customer(email),
        "description": "Test payment request",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# Map event types → sample data generators
_DATA_GENERATORS: Dict[str, Any] = {
    # Charge events
    "charge.success": lambda ref, amt, email: _make_charge_data(ref, amt, email, "success"),
    # Dispute events
    "charge.dispute.create": lambda _r, amt, _e: _make_dispute_data(amt),
    "charge.dispute.remind": lambda _r, amt, _e: _make_dispute_data(amt),
    "charge.dispute.resolve": lambda _r, amt, _e: {**_make_dispute_data(amt), "status": "resolved", "resolution": "merchant-accepted"},
    # Customer identification events
    "customeridentification.success": lambda _r, _a, email: _make_customeridentification_data(email, "success"),
    "customeridentification.failed": lambda _r, _a, email: _make_customeridentification_data(email, "failed"),
    # Dedicated account events
    "dedicatedaccount.assign.success": lambda _r, _a, email: _make_dedicatedaccount_data(email, "success"),
    "dedicatedaccount.assign.failed": lambda _r, _a, email: _make_dedicatedaccount_data(email, "failed"),
    # Invoice events
    "invoice.create": lambda _r, amt, email: _make_invoice_data(email, amt, "pending"),
    "invoice.update": lambda _r, amt, email: _make_invoice_data(email, amt, "success"),
    "invoice.payment_failed": lambda _r, amt, email: _make_invoice_data(email, amt, "failed"),
    # Payment request events
    "paymentrequest.pending": lambda _r, amt, email: _make_paymentrequest_data(email, amt, "pending"),
    "paymentrequest.success": lambda _r, amt, email: _make_paymentrequest_data(email, amt, "success"),
    # Refund events
    "refund.pending": lambda _r, amt, _e: {**_make_refund_data(amt), "status": "pending"},
    "refund.processing": lambda _r, amt, _e: {**_make_refund_data(amt), "status": "processing"},
    "refund.processed": lambda _r, amt, _e: _make_refund_data(amt),
    "refund.failed": lambda _r, amt, _e: {**_make_refund_data(amt), "status": "failed"},
    # Subscription events
    "subscription.create": lambda _r, _a, email: _make_subscription_data(email),
    "subscription.disable": lambda _r, _a, email: {**_make_subscription_data(email), "status": "cancelled"},
    "subscription.not_renew": lambda _r, _a, email: {**_make_subscription_data(email), "status": "non-renewing"},
    "subscription.expiring_cards": lambda _r, _a, email: {**_make_subscription_data(email), "status": "active", "card_expiry_month": "03", "card_expiry_year": "2026"},
    # Transfer events
    "transfer.success": lambda _r, amt, _e: _make_transfer_data(amt, "success"),
    "transfer.failed": lambda _r, amt, _e: _make_transfer_data(amt, "failed"),
    "transfer.reversed": lambda _r, amt, _e: _make_transfer_data(amt, "reversed"),
}


class Command(BaseCommand):
    help = "Send a simulated Paystack webhook event to your local server."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "event_type",
            nargs="?",
            type=str,
            help="Webhook event type (e.g. charge.success, transfer.failed)",
        )
        parser.add_argument(
            "--url",
            type=str,
            default="http://localhost:8000/webhooks/paystack/",
            help="Webhook endpoint URL (default: http://localhost:8000/webhooks/paystack/)",
        )
        parser.add_argument(
            "--data",
            type=str,
            help="Custom JSON data payload (overrides generated sample data)",
        )
        parser.add_argument(
            "--reference",
            type=str,
            default=None,
            help="Transaction reference (auto-generated if omitted)",
        )
        parser.add_argument(
            "--amount",
            type=int,
            default=50000,
            help="Amount in kobo (default: 50000)",
        )
        parser.add_argument(
            "--email",
            type=str,
            default="test@example.com",
            help="Customer email (default: test@example.com)",
        )
        parser.add_argument(
            "--list",
            action="store_true",
            dest="list_events",
            help="List all supported webhook event types and exit",
        )

    def handle(self, *args, **options) -> None:
        if options["list_events"]:
            self._list_events()
            return

        event_type: str | None = options["event_type"]
        if not event_type:
            raise CommandError(
                "You must specify an event type, or use --list to see all options."
            )

        secret_key = paystack_settings.SECRET_KEY
        if not secret_key:
            raise CommandError(
                "PAYSTACK['SECRET_KEY'] is not configured in your Django settings."
            )

        reference = options["reference"] or f"test_{uuid.uuid4().hex[:10]}"
        amount: int = options["amount"]
        email: str = options["email"]
        webhook_url: str = options["url"]

        # Build payload
        if options["data"]:
            try:
                data = json.loads(options["data"])
            except json.JSONDecodeError as exc:
                raise CommandError(f"Invalid JSON in --data: {exc}")
        elif event_type in _DATA_GENERATORS:
            data = _DATA_GENERATORS[event_type](reference, amount, email)
        else:
            # Minimal fallback
            data = {"reference": reference,
                    "amount": amount, "status": "success"}

        payload = {"event": event_type, "data": data}
        payload_bytes = json.dumps(payload).encode("utf-8")

        # Sign
        signature = hmac.new(
            secret_key.encode("utf-8"),
            payload_bytes,
            hashlib.sha512,
        ).hexdigest()

        self.stdout.write(f"\nEvent:     {event_type}")
        self.stdout.write(f"Target:    {webhook_url}")
        self.stdout.write(f"Amount:    {amount} kobo")
        self.stdout.write(f"Reference: {data.get('reference', 'N/A')}")

        # Send via stdlib (no requests dependency)
        req = Request(
            webhook_url,
            data=payload_bytes,
            headers={
                "Content-Type": "application/json",
                "X-Paystack-Signature": signature,
            },
            method="POST",
        )

        try:
            with urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                self.stdout.write(
                    self.style.SUCCESS(f"\n✓ {resp.status} — {body}")
                )
        except URLError as exc:
            self.stderr.write(
                self.style.ERROR(f"\n✗ Request failed: {exc.reason}")
            )
            self.stderr.write(
                "  Is your Django server running? "
                "Try: python manage.py runserver"
            )

    # ------------------------------------------------------------------

    def _list_events(self) -> None:
        """Pretty-print all WebhookEvent members grouped by category."""
        categories: Dict[str, list] = {
            "Charge": [],
            "Transfer": [],
            "Subscription": [],
            "Invoice": [],
            "Customer Identification": [],
            "Refund": [],
            "Dispute": [],
            "Dedicated Account": [],
            "Payment Request": [],
        }

        for event in WebhookEvent:
            value = event.value
            if value.startswith("charge.dispute"):
                categories["Dispute"].append(value)
            elif value.startswith("charge"):
                categories["Charge"].append(value)
            elif value.startswith("transfer"):
                categories["Transfer"].append(value)
            elif value.startswith("subscription"):
                categories["Subscription"].append(value)
            elif value.startswith("invoice"):
                categories["Invoice"].append(value)
            elif value.startswith("customeridentification"):
                categories["Customer Identification"].append(value)
            elif value.startswith("refund"):
                categories["Refund"].append(value)
            elif value.startswith("dedicatedaccount"):
                categories["Dedicated Account"].append(value)
            elif value.startswith("paymentrequest"):
                categories["Payment Request"].append(value)

        sep = "━" * 60
        self.stdout.write(
            self.style.SUCCESS("\nPaystack Webhook Event Types\n")
        )
        self.stdout.write(sep)

        for category, events in categories.items():
            if not events:
                continue
            self.stdout.write(f"\n  {category}:")
            for ev in events:
                has_sample = "●" if ev in _DATA_GENERATORS else "○"
                self.stdout.write(f"    {has_sample} {ev}")

        self.stdout.write(f"\n{sep}")
        self.stdout.write(
            "  ● = sample data included   ○ = use --data for custom payload\n")
        self.stdout.write("  Usage:")
        self.stdout.write(
            "    python manage.py paystack_webhook_event charge.success")
        self.stdout.write(
            "    python manage.py paystack_webhook_event transfer.failed --amount 100000\n"
        )
