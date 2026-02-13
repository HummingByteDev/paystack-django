
import uuid
import hashlib
from typing import Optional
from decimal import Decimal


def generate_reference(prefix: str = 'PS') -> str:
    """
    Generate a unique transaction reference

    Args:
        prefix: Prefix for the reference

    Returns:
        Unique reference string
    """
    unique_id = uuid.uuid4().hex[:12].upper()
    return f"{prefix}{unique_id}"


def kobo_to_naira(kobo: int) -> Decimal:
    """
    Convert kobo to naira

    Args:
        kobo: Amount in kobo

    Returns:
        Amount in naira
    """
    return Decimal(kobo) / 100


def naira_to_kobo(naira: float) -> int:
    """
    Convert naira to kobo

    Args:
        naira: Amount in naira

    Returns:
        Amount in kobo
    """
    return int(naira * 100)


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify Paystack webhook signature

    Args:
        payload: Raw request body
        signature: X-Paystack-Signature header value
        secret: Webhook secret key

    Returns:
        True if signature is valid
    """
    import hmac
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)


def format_amount(amount: int, currency: str = 'NGN') -> str:
    """
    Format amount for display

    Args:
        amount: Amount in kobo
        currency: Currency code

    Returns:
        Formatted amount string
    """
    symbols = {
        'NGN': '₦',
        'GHS': 'GH₵',
        'ZAR': 'R',
        'USD': '$',
    }
    symbol = symbols.get(currency, currency)
    naira_amount = kobo_to_naira(amount)
    return f"{symbol}{naira_amount:,.2f}"
