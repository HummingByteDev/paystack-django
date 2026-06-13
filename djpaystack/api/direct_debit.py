"""
Direct Debit API
https://paystack.com/docs/api/directdebit/

Note: customer-scoped Direct Debit onboarding (initialize, activation charge,
mandate authorizations) lives on the Customer API; see ``CustomerAPI``.
"""

from typing import Any, Dict, List, Optional

from .base import BaseAPI


class DirectDebitAPI(BaseAPI):
    """Paystack Direct Debit API (account-level operations)."""

    def trigger_activation_charge(self, customer_ids: List[int]) -> Dict[str, Any]:
        """Trigger an activation charge for one or more customers' mandates.

        Args:
            customer_ids: List of customer IDs to charge for mandate activation.
        """
        return self._put("directdebit/activation-charge", data={"customer_ids": customer_ids})

    def list_mandate_authorizations(
        self,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
        per_page: int = 50,
    ) -> Dict[str, Any]:
        """List direct debit mandate authorizations (cursor-paginated).

        Args:
            cursor: Pagination cursor returned by a previous call.
            status: Filter by mandate status (e.g. ``pending``, ``active``).
            per_page: Number of records per page.
        """
        params = self._build_query_params(cursor=cursor, status=status, per_page=per_page)
        return self._get("directdebit/mandate-authorizations", params=params)
