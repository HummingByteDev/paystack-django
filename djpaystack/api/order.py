"""
Order API
https://paystack.com/docs/api/
"""

from typing import Any, Dict, List, Optional

from .base import BaseAPI


class OrderAPI(BaseAPI):
    """Paystack Order API for storefront/commerce orders."""

    def create(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone: str,
        currency: str,
        items: List[Dict[str, Any]],
        shipping: Dict[str, Any],
        is_gift: Optional[bool] = None,
        pay_for_me: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create an order.

        Args:
            email: Customer's email address.
            first_name: Customer's first name.
            last_name: Customer's last name.
            phone: Customer's phone number.
            currency: Currency code (e.g. ``NGN``).
            items: List of order line items.
            shipping: Shipping details.
            is_gift: Whether the order is a gift.
            pay_for_me: Whether a third party should pay.
        """
        data = self._build_query_params(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            currency=currency,
            items=items,
            shipping=shipping,
            is_gift=is_gift,
            pay_for_me=pay_for_me,
            **kwargs,
        )
        return self._post("order", data=data)

    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List orders (``from_date``/``to_date`` map to ``from``/``to``)."""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate("order", params=params, per_page=per_page, page=page)

    def fetch(self, id: str) -> Dict[str, Any]:
        """Fetch a single order by id."""
        return self._get(f"order/{id}")

    def fetch_product_orders(self, id: str) -> Dict[str, Any]:
        """Fetch orders for a given product id."""
        return self._get(f"order/product/{id}")

    def validate(self, code: str) -> Dict[str, Any]:
        """Validate an order by code."""
        return self._get(f"order/{code}/validate")
