<<<<<<< HEAD
import hashlib
=======

import hashlib
import hmac
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f
import uuid
from decimal import Decimal
from typing import Optional, Union


def generate_reference(prefix: str = "PS") -> str:
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


def naira_to_kobo(naira: Union[float, Decimal]) -> int:
    """
    Convert naira to kobo

    Args:
        naira: Amount in naira (float or Decimal)

    Returns:
        Amount in kobo
    """
    return int(Decimal(str(naira)) * 100)


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
<<<<<<< HEAD
    import hmac

    computed_signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha512).hexdigest()
=======
    computed_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha512
    ).hexdigest()
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f
    return hmac.compare_digest(computed_signature, signature)


def format_amount(amount: int, currency: str = "NGN") -> str:
    """
    Format amount for display

    Args:
        amount: Amount in kobo
        currency: Currency code

    Returns:
        Formatted amount string
    """
    symbols = {
        "NGN": "₦",
        "GHS": "GH₵",
        "ZAR": "R",
        "USD": "$",
    }
    symbol = symbols.get(currency, currency)
    naira_amount = kobo_to_naira(amount)
    return f"{symbol}{naira_amount:,.2f}"
