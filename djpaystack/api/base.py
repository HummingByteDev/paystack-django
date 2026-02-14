"""
Base API class for all Paystack API endpoints
"""
from typing import Dict, Any, Optional, List, Union


class BaseAPI:
    """
    Base class for all Paystack API endpoints
    """

    def __init__(self, client):
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
        page: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Helper method for paginated requests

        Args:
            endpoint: API endpoint
            params: Query parameters
            per_page: Number of items per page
            page: Specific page number (None for all pages)

        Returns:
            Response data with results
        """
        params = params or {}
        params['perPage'] = per_page

        if page is not None:
            params['page'] = page
            return self._get(endpoint, params=params)

        # Fetch all pages if page is None
        all_results = []
        current_page = 1

        while True:
            params['page'] = current_page
            response = self._get(endpoint, params=params)

            data = response.get('data', [])
            if isinstance(data, list):
                all_results.extend(data)
            else:
                # Handle single object response
                return response

            meta = response.get('meta', {})
            if not meta or current_page >= meta.get('pageCount', 1):
                break

            current_page += 1

        # Return combined results
        return {
            'status': True,
            'message': 'Success',
            'data': all_results
        }

    def _build_query_params(self, **kwargs) -> Dict[str, Any]:
        """Build query parameters, filtering out None values"""
        return {k: v for k, v in kwargs.items() if v is not None}
