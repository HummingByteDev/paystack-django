"""
Base API class for all Paystack API endpoints
"""

from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Union

if TYPE_CHECKING:
    from ..client import PaystackClient


class BaseAPI:
    """
    Base class for all Paystack API endpoints
    """

    #: map Python-friendly keyword names to Paystack wire parameter
    #: names. ``from``/``to`` are Python keywords, so callers use
    #: ``from_date``/``to_date`` which must be renamed before transmission.
    _PARAM_NAME_MAP: Dict[str, str] = {"from_date": "from", "to_date": "to"}

    def __init__(self, client: "PaystackClient") -> None:
        """
        Initialize API endpoint

        Args:
            client: PaystackClient instance
        """
        self.client = client

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self.client.get(endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """Make POST request (accepts single dict or list for bulk endpoints)"""
        return self.client.post(endpoint, data=data)

    def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self.client.put(endpoint, data=data)

    def _delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make DELETE request (optional body)"""
        return self.client.delete(endpoint, data=data)

    def _paginate(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        per_page: int = 50,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Fetch a **single** page of a list endpoint.

        this returns one page (the first when ``page`` is omitted) and
        preserves Paystack's ``meta`` block so callers can paginate. It does NOT
        eagerly download the entire dataset (which could exhaust memory on large
        accounts). To stream every record lazily, use :meth:`_iterate` (exposed
        on resources as ``iterate``/``iter_all``).

        Args:
            endpoint: API endpoint.
            params: Query parameters.
            per_page: Number of items per page.
            page: Page number (defaults to 1).

        Returns:
            The raw Paystack response for the requested page (including ``meta``).
        """
        params = dict(params or {})
        params["perPage"] = per_page
        params["page"] = page if page is not None else 1
        return self._get(endpoint, params=params)

    def _iterate(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        per_page: int = 50,
    ) -> Iterator[Dict[str, Any]]:
        """Lazily yield every record across all pages of a list endpoint.

        Pages are fetched on demand, so memory usage stays bounded regardless of
        how many records exist.
        """
        params = dict(params or {})
        params["perPage"] = per_page
        page = 1
        while True:
            params["page"] = page
            response = self._get(endpoint, params=params)
            data = response.get("data", [])
            if not isinstance(data, list):
                return
            for item in data:
                yield item

            meta = response.get("meta") or {}
            page_count = meta.get("pageCount")
            if page_count is not None:
                if page >= page_count:
                    return
            elif len(data) < per_page:
                # No meta available: a short page means we're done.
                return
            page += 1

    def _build_query_params(self, **kwargs: Any) -> Dict[str, Any]:
        """Build query parameters, filtering out None values and mapping
        Python-friendly names to Paystack wire names."""
        params: Dict[str, Any] = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            params[self._PARAM_NAME_MAP.get(key, key)] = value
        return params
