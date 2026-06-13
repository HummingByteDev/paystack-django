"""
Storefront API
https://paystack.com/docs/api/
"""

from typing import Any, Dict, List, Optional

from .base import BaseAPI


class StorefrontAPI(BaseAPI):
    """Paystack Storefront API for hosted commerce storefronts."""

    def create(
        self,
        name: str,
        slug: str,
        currency: str,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create a storefront."""
        data = self._build_query_params(
            name=name, slug=slug, currency=currency, description=description, **kwargs
        )
        return self._post("storefront", data=data)

    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List storefronts."""
        params = self._build_query_params(status=status)
        return self._paginate("storefront", params=params, per_page=per_page, page=page)

    def fetch(self, id: str) -> Dict[str, Any]:
        """Fetch a single storefront by id."""
        return self._get(f"storefront/{id}")

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Update a storefront."""
        data = self._build_query_params(name=name, slug=slug, description=description, **kwargs)
        return self._put(f"storefront/{id}", data=data)

    def delete(self, id: str) -> Dict[str, Any]:
        """Delete a storefront."""
        return self._delete(f"storefront/{id}")

    def verify_slug(self, slug: str) -> Dict[str, Any]:
        """Check whether a storefront slug is available."""
        return self._get(f"storefront/verify/{slug}")

    def fetch_orders(self, id: str) -> Dict[str, Any]:
        """Fetch orders belonging to a storefront."""
        return self._get(f"storefront/{id}/order")

    def add_products(self, id: str, products: List[int]) -> Dict[str, Any]:
        """Add products to a storefront."""
        return self._post(f"storefront/{id}/product", data={"products": products})

    def list_products(self, id: str) -> Dict[str, Any]:
        """List products in a storefront."""
        return self._get(f"storefront/{id}/product")

    def publish(self, id: str) -> Dict[str, Any]:
        """Publish a storefront."""
        return self._post(f"storefront/{id}/publish", data={})

    def duplicate(self, id: str) -> Dict[str, Any]:
        """Duplicate a storefront."""
        return self._post(f"storefront/{id}/duplicate", data={})
