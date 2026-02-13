from typing import Dict, Any, Optional, List
from .base import BaseAPI


class TerminalAPI(BaseAPI):
    """Terminal API"""

    def send_event(self, terminal_id: str, type: str, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send event to terminal"""
        payload = {'type': type, 'action': action, 'data': data}
        return self._post(f'terminal/{terminal_id}/event', data=payload)

    def fetch_event_status(self, terminal_id: str, event_id: str) -> Dict[str, Any]:
        """Fetch terminal event status"""
        return self._get(f'terminal/{terminal_id}/event/{event_id}')

    def fetch_terminal_status(self, terminal_id: str) -> Dict[str, Any]:
        """Fetch terminal status"""
        return self._get(f'terminal/{terminal_id}/presence')

    def list(self, per_page: int = 50, page: Optional[int] = None) -> Dict[str, Any]:
        """List terminals"""
        return self._paginate('terminal', per_page=per_page, page=page)

    def fetch(self, terminal_id: str) -> Dict[str, Any]:
        """Fetch terminal details"""
        return self._get(f'terminal/{terminal_id}')

    def update(self, terminal_id: str, name: str, address: str) -> Dict[str, Any]:
        """Update terminal"""
        data = {'name': name, 'address': address}
        return self._put(f'terminal/{terminal_id}', data=data)

    def commission(self, serial_number: str) -> Dict[str, Any]:
        """Commission terminal"""
        data = {'serial_number': serial_number}
        return self._post('terminal/commission_device', data=data)

    def decommission(self, serial_number: str) -> Dict[str, Any]:
        """Decommission terminal"""
        data = {'serial_number': serial_number}
        return self._post('terminal/decommission_device', data=data)
