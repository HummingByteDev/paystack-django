"""
Virtual Terminal API
https://paystack.com/docs/api/virtual-terminal/
"""

from typing import Any, Dict, List, Optional

from .base import BaseAPI


class VirtualTerminalAPI(BaseAPI):
    """
    Paystack Virtual Terminal API

    Virtual Terminals allow you to accept in-person payments without a physical
    POS device, by sharing a payment link/QR with customers.
    """

    def create(
        self,
        name: str,
        destinations: List[Dict[str, Any]],
        split_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create a virtual terminal.

        Args:
            name: Name of the virtual terminal.
            destinations: List of notification destinations, e.g.
                ``[{"target": "+234...", "name": "Sales"}]``.
            split_code: Optional split code for revenue sharing.
            metadata: Optional metadata.
        """
        data = self._build_query_params(
            name=name,
            destinations=destinations,
            split_code=split_code,
            metadata=metadata,
            **kwargs,
        )
        return self._post("virtual_terminal", data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None) -> Dict[str, Any]:
        """List virtual terminals."""
        return self._paginate("virtual_terminal", per_page=per_page, page=page)

    def fetch(self, code: str) -> Dict[str, Any]:
        """Fetch a single virtual terminal by code."""
        return self._get(f"virtual_terminal/{code}")

    def update(self, code: str, name: str) -> Dict[str, Any]:
        """Update a virtual terminal's name."""
        return self._put(f"virtual_terminal/{code}", data={"name": name})

    def deactivate(self, code: str) -> Dict[str, Any]:
        """Deactivate a virtual terminal."""
        return self._put(f"virtual_terminal/{code}/deactivate", data={})

    def assign_destination(self, code: str, destinations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assign notification destinations to a virtual terminal."""
        return self._post(
            f"virtual_terminal/{code}/destination/assign",
            data={"destinations": destinations},
        )

    def unassign_destination(self, code: str, targets: List[Any]) -> Dict[str, Any]:
        """Unassign notification destinations from a virtual terminal."""
        return self._post(
            f"virtual_terminal/{code}/destination/unassign",
            data={"targets": targets},
        )

    def add_split_code(self, code: str, split_code: str) -> Dict[str, Any]:
        """Add a transaction split code to a virtual terminal."""
        return self._put(f"virtual_terminal/{code}/split_code", data={"split_code": split_code})

    def remove_split_code(self, code: str, split_code: str) -> Dict[str, Any]:
        """Remove a transaction split code from a virtual terminal."""
        return self._delete(f"virtual_terminal/{code}/split_code", data={"split_code": split_code})
