from typing import Dict, Any, Optional, List
from .base import BaseAPI


class VirtualTerminalAPI(BaseAPI):
    """Virtual Terminal API"""

    def send_event(self, terminal_id: str, type: str, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send event to virtual terminal"""
        payload = {'type': type, 'action': action, 'data': data}
        return self._post(f'virtual_terminal/{terminal_id}/event', data=payload)
