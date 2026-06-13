"""
Core Paystack API client
"""

import logging
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .api import (
    ApplePayAPI,
    BulkChargeAPI,
    ChargeAPI,
    CustomerAPI,
    DedicatedAccountAPI,
    DirectDebitAPI,
    DisputeAPI,
    IntegrationAPI,
    MiscellaneousAPI,
    OrderAPI,
    PageAPI,
    PaymentRequestAPI,
    PlanAPI,
    ProductAPI,
    RefundAPI,
    SettlementAPI,
    SplitAPI,
    StorefrontAPI,
    SubaccountAPI,
    SubscriptionAPI,
    TerminalAPI,
    TransactionAPI,
    TransferAPI,
    TransferControlAPI,
    TransferRecipientAPI,
    VerificationAPI,
    VirtualTerminalAPI,
)
from .exceptions import (
    PaystackAPIError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)
from .settings import paystack_settings

logger = logging.getLogger("djpaystack")


class PaystackClient:
    """
    Main Paystack API client with all service endpoints
    """

    def __init__(self, secret_key: Optional[str] = None, public_key: Optional[str] = None):
        """
        Initialize Paystack client

        Args:
            secret_key: Optional Paystack secret key (overrides settings)
            public_key: Optional Paystack public key (overrides settings)
        """
        self.secret_key = secret_key or paystack_settings.SECRET_KEY
        self.public_key = public_key or paystack_settings.PUBLIC_KEY
        self.base_url = paystack_settings.BASE_URL
        self.timeout = paystack_settings.TIMEOUT

        if not self.secret_key:
            raise PaystackAuthenticationError("Paystack secret key is required")

        # Setup session with retry logic
        self.session = self._create_session()

        # Initialize API endpoints
        self.transactions = TransactionAPI(self)
        self.splits = SplitAPI(self)
        self.terminal = TerminalAPI(self)
        self.virtual_terminal = VirtualTerminalAPI(self)
        self.customers = CustomerAPI(self)
        self.direct_debit = DirectDebitAPI(self)
        self.dedicated_accounts = DedicatedAccountAPI(self)
        self.apple_pay = ApplePayAPI(self)
        self.subaccounts = SubaccountAPI(self)
        self.plans = PlanAPI(self)
        self.subscriptions = SubscriptionAPI(self)
        self.products = ProductAPI(self)
        self.pages = PageAPI(self)
        self.payment_requests = PaymentRequestAPI(self)
        self.settlements = SettlementAPI(self)
        self.transfer_recipients = TransferRecipientAPI(self)
        self.transfers = TransferAPI(self)
        self.transfer_control = TransferControlAPI(self)
        self.bulk_charges = BulkChargeAPI(self)
        self.integration = IntegrationAPI(self)
        self.charge = ChargeAPI(self)
        self.disputes = DisputeAPI(self)
        self.refunds = RefundAPI(self)
        self.verification = VerificationAPI(self)
        self.miscellaneous = MiscellaneousAPI(self)
        self.order = OrderAPI(self)
        self.storefront = StorefrontAPI(self)

    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic"""
        session = requests.Session()

        # only retry idempotent methods automatically. POST/PUT
        # are intentionally excluded — retrying a charge/transfer that already
        # succeeded server-side but returned a transient error can double-charge.
        retry_strategy = Retry(
            total=paystack_settings.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # identify SDK traffic to Paystack.
        from . import __version__

        session.headers.update({"User-Agent": f"paystack-django/{__version__}"})

        return session

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]], Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Paystack API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: URL query parameters
            **kwargs: Additional arguments for requests

        Returns:
            Response data dictionary

        Raises:
            PaystackAPIError: If API returns error
            PaystackNetworkError: If network request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()

        # Log request if enabled
        if paystack_settings.LOG_REQUESTS:
            logger.info(f"Paystack Request: {method} {url}")
            if data:
                logger.debug(f"Request Data: {data}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=self.timeout,
                verify=paystack_settings.VERIFY_SSL,
                **kwargs,
            )

            # Log response if enabled
            if paystack_settings.LOG_RESPONSES:
                logger.info(f"Paystack Response: {response.status_code}")
                logger.debug(f"Response Data: {response.text}")

            # Parse JSON response
            try:
                response_data = response.json()
            except ValueError:
                raise PaystackAPIError(
                    f"Invalid JSON response from Paystack: {response.text}",
                    status_code=response.status_code,
                    response=response,
                )

            # Check for errors (route auth failures to the dedicated
            # exception so callers can distinguish them; both remain subclasses
            # of PaystackError for backwards compatibility).
            if not response_data.get("status"):
                error_message = response_data.get("message", "Unknown error")
                if response.status_code in (401, 403):
                    raise PaystackAuthenticationError(error_message, response=response_data)
                raise PaystackAPIError(
                    error_message, status_code=response.status_code, response=response_data
                )

            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack network error: {str(e)}")
            raise PaystackNetworkError(f"Network request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self.request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """Make POST request (accepts a single object or a list for bulk endpoints)"""
        return self.request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self.request("PUT", endpoint, data=data)

    def delete(
        self, endpoint: str, data: Optional[Any] = None, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make DELETE request (accepts optional body/params)"""
        return self.request("DELETE", endpoint, data=data, params=params)

    def close(self):
        """Close session"""
        if self.session:
            self.session.close()
