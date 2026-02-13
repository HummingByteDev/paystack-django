"""
Transactions API
https://paystack.com/docs/api/transaction/
"""
from typing import Dict, Any, Optional, List
from .base import BaseAPI


class TransactionAPI(BaseAPI):
    """
    Paystack Transactions API

    The Transactions API allows you create and manage payments on your integration.
    """

    def initialize(
        self,
        email: str,
        amount: int,
        currency: Optional[str] = None,
        reference: Optional[str] = None,
        callback_url: Optional[str] = None,
        plan: Optional[str] = None,
        invoice_limit: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channels: Optional[List[str]] = None,
        split_code: Optional[str] = None,
        subaccount: Optional[str] = None,
        transaction_charge: Optional[int] = None,
        bearer: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Initialize a transaction

        Args:
            email: Customer's email address
            amount: Amount in kobo (multiply naira by 100)
            currency: Currency (NGN, GHS, ZAR, or USD)
            reference: Unique transaction reference
            callback_url: URL to redirect after payment
            plan: Plan code for subscription
            invoice_limit: Number of times to charge customer during subscription
            metadata: Additional transaction data
            channels: Payment channels to control (card, bank, ussd, qr, mobile_money, bank_transfer)
            split_code: Transaction split code
            subaccount: Subaccount code
            transaction_charge: Amount to charge subaccount
            bearer: Who bears Paystack charges (account, subaccount)

        Returns:
            Response with authorization_url and access_code
        """
        data = self._build_query_params(
            email=email,
            amount=amount,
            currency=currency,
            reference=reference,
            callback_url=callback_url,
            plan=plan,
            invoice_limit=invoice_limit,
            metadata=metadata,
            channels=channels,
            split_code=split_code,
            subaccount=subaccount,
            transaction_charge=transaction_charge,
            bearer=bearer,
            **kwargs
        )
        return self._post('transaction/initialize', data=data)

    def verify(self, reference: str) -> Dict[str, Any]:
        """
        Verify a transaction

        Args:
            reference: Transaction reference

        Returns:
            Transaction details
        """
        return self._get(f'transaction/verify/{reference}')

    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        customer: Optional[int] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        amount: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List transactions

        Args:
            per_page: Records per page
            page: Page number
            customer: Customer ID
            status: Transaction status (failed, success, abandoned)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            amount: Transaction amount

        Returns:
            List of transactions
        """
        params = self._build_query_params(
            customer=customer,
            status=status,
            from_date=from_date,
            to_date=to_date,
            amount=amount
        )
        return self._paginate('transaction', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_reference: str) -> Dict[str, Any]:
        """
        Fetch a single transaction

        Args:
            id_or_reference: Transaction ID or reference

        Returns:
            Transaction details
        """
        return self._get(f'transaction/{id_or_reference}')

    def charge_authorization(
        self,
        authorization_code: str,
        email: str,
        amount: int,
        reference: Optional[str] = None,
        currency: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channels: Optional[List[str]] = None,
        subaccount: Optional[str] = None,
        transaction_charge: Optional[int] = None,
        bearer: Optional[str] = None,
        queue: Optional[bool] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Charge an authorization

        Args:
            authorization_code: Authorization code for card
            email: Customer's email
            amount: Amount in kobo
            reference: Unique transaction reference
            currency: Currency code
            metadata: Additional transaction data
            channels: Payment channels
            subaccount: Subaccount code
            transaction_charge: Amount to charge subaccount
            bearer: Who bears Paystack charges
            queue: Queue transaction for later processing

        Returns:
            Transaction response
        """
        data = self._build_query_params(
            authorization_code=authorization_code,
            email=email,
            amount=amount,
            reference=reference,
            currency=currency,
            metadata=metadata,
            channels=channels,
            subaccount=subaccount,
            transaction_charge=transaction_charge,
            bearer=bearer,
            queue=queue,
            **kwargs
        )
        return self._post('transaction/charge_authorization', data=data)

    def check_authorization(
        self,
        authorization_code: str,
        email: str,
        amount: int,
        currency: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if authorization is valid for amount

        Args:
            authorization_code: Authorization code
            email: Customer's email
            amount: Amount in kobo
            currency: Currency code

        Returns:
            Validation response
        """
        data = self._build_query_params(
            authorization_code=authorization_code,
            email=email,
            amount=amount,
            currency=currency
        )
        return self._post('transaction/check_authorization', data=data)

    def timeline(self, id_or_reference: str) -> Dict[str, Any]:
        """
        View transaction timeline

        Args:
            id_or_reference: Transaction ID or reference

        Returns:
            Transaction timeline
        """
        return self._get(f'transaction/timeline/{id_or_reference}')

    def totals(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get transaction totals

        Args:
            per_page: Records per page
            page: Page number
            from_date: Start date
            to_date: End date

        Returns:
            Transaction totals
        """
        params = self._build_query_params(
            perPage=per_page,
            page=page,
            from_date=from_date,
            to_date=to_date
        )
        return self._get('transaction/totals', params=params)

    def export(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        customer: Optional[int] = None,
        status: Optional[str] = None,
        currency: Optional[str] = None,
        amount: Optional[int] = None,
        settled: Optional[bool] = None,
        settlement: Optional[int] = None,
        payment_page: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Export transactions

        Args:
            per_page: Records per page
            page: Page number
            from_date: Start date
            to_date: End date
            customer: Customer ID
            status: Transaction status
            currency: Currency
            amount: Amount
            settled: Settlement status
            settlement: Settlement ID
            payment_page: Payment page ID

        Returns:
            Export response with download link
        """
        params = self._build_query_params(
            perPage=per_page,
            page=page,
            from_date=from_date,
            to_date=to_date,
            customer=customer,
            status=status,
            currency=currency,
            amount=amount,
            settled=settled,
            settlement=settlement,
            payment_page=payment_page
        )
        return self._get('transaction/export', params=params)

    def partial_debit(
        self,
        authorization_code: str,
        currency: str,
        amount: int,
        email: str,
        reference: Optional[str] = None,
        at_least: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Partial debit allows you to retrieve part of a payment from a customer

        Args:
            authorization_code: Authorization code
            currency: Currency
            amount: Amount in kobo
            email: Customer email
            reference: Transaction reference
            at_least: Minimum amount to charge

        Returns:
            Transaction response
        """
        data = self._build_query_params(
            authorization_code=authorization_code,
            currency=currency,
            amount=amount,
            email=email,
            reference=reference,
            at_least=at_least
        )
        return self._post('transaction/partial_debit', data=data)
