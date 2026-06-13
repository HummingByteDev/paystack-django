"""
Contract tests for the Paystack API endpoint clients.

Each test asserts the exact verb + path (and key params) sent on the wire,
validated against the official Paystack OpenAPI specification.

Covers: Virtual Terminal, Direct Debit, Order,
Storefront, Customer authorizations/direct-debit, and the
missing single endpoints.
"""

from unittest.mock import Mock, patch

import pytest

from djpaystack import PaystackClient


@pytest.fixture
def client():
    with patch("djpaystack.client.paystack_settings") as s:
        s.SECRET_KEY = "sk_test_xxxxx"
        s.BASE_URL = "https://api.paystack.co"
        s.TIMEOUT = 30
        s.MAX_RETRIES = 3
        s.VERIFY_SSL = True
        yield PaystackClient()


@pytest.fixture
def call(client):
    """Patch the session and return a helper that calls then returns (method, url, kwargs)."""
    mock_request = patch.object(client.session, "request").start()
    resp = Mock()
    resp.json.return_value = {"status": True, "message": "ok", "data": []}
    resp.status_code = 200
    mock_request.return_value = resp

    def _last():
        _, kwargs = mock_request.call_args
        return kwargs["method"], kwargs["url"], kwargs

    yield client, _last
    patch.stopall()


# --------------------------------------------------------------------------- #
# Virtual Terminal
# --------------------------------------------------------------------------- #
class TestVirtualTerminal:
    def test_create(self, call):
        client, last = call
        client.virtual_terminal.create(
            name="VT", destinations=[{"target": "+234", "name": "Sales"}]
        )
        method, url, kw = last()
        assert method == "POST" and url.endswith("/virtual_terminal")
        assert kw["json"]["name"] == "VT"

    def test_list(self, call):
        client, last = call
        client.virtual_terminal.list(page=1)
        method, url, _ = last()
        assert method == "GET" and url.endswith("/virtual_terminal")

    def test_fetch(self, call):
        client, last = call
        client.virtual_terminal.fetch("VT_1")
        method, url, _ = last()
        assert method == "GET" and url.endswith("/virtual_terminal/VT_1")

    def test_update(self, call):
        client, last = call
        client.virtual_terminal.update("VT_1", name="New")
        method, url, kw = last()
        assert method == "PUT" and url.endswith("/virtual_terminal/VT_1")
        assert kw["json"] == {"name": "New"}

    def test_deactivate(self, call):
        client, last = call
        client.virtual_terminal.deactivate("VT_1")
        method, url, _ = last()
        assert method == "PUT" and url.endswith("/virtual_terminal/VT_1/deactivate")

    def test_assign_destination(self, call):
        client, last = call
        client.virtual_terminal.assign_destination("VT_1", [{"target": "+234", "name": "x"}])
        method, url, kw = last()
        assert method == "POST" and url.endswith("/virtual_terminal/VT_1/destination/assign")
        assert "destinations" in kw["json"]

    def test_unassign_destination(self, call):
        client, last = call
        client.virtual_terminal.unassign_destination("VT_1", ["+234"])
        method, url, kw = last()
        assert method == "POST" and url.endswith("/virtual_terminal/VT_1/destination/unassign")
        assert kw["json"] == {"targets": ["+234"]}

    def test_add_split_code(self, call):
        client, last = call
        client.virtual_terminal.add_split_code("VT_1", "SPL_1")
        method, url, kw = last()
        assert method == "PUT" and url.endswith("/virtual_terminal/VT_1/split_code")
        assert kw["json"] == {"split_code": "SPL_1"}

    def test_remove_split_code(self, call):
        client, last = call
        client.virtual_terminal.remove_split_code("VT_1", "SPL_1")
        method, url, _ = last()
        assert method == "DELETE" and url.endswith("/virtual_terminal/VT_1/split_code")


# --------------------------------------------------------------------------- #
# Direct Debit
# --------------------------------------------------------------------------- #
class TestDirectDebit:
    def test_trigger_activation_charge(self, call):
        client, last = call
        client.direct_debit.trigger_activation_charge([1, 2])
        method, url, kw = last()
        assert method == "PUT" and url.endswith("/directdebit/activation-charge")
        assert kw["json"] == {"customer_ids": [1, 2]}

    def test_list_mandate_authorizations(self, call):
        client, last = call
        client.direct_debit.list_mandate_authorizations(status="active", per_page=10)
        method, url, kw = last()
        assert method == "GET" and url.endswith("/directdebit/mandate-authorizations")
        assert kw["params"]["status"] == "active"
        assert kw["params"]["per_page"] == 10


# --------------------------------------------------------------------------- #
# Order
# --------------------------------------------------------------------------- #
class TestOrder:
    def test_create(self, call):
        client, last = call
        client.order.create(
            email="a@b.com",
            first_name="A",
            last_name="B",
            phone="+234",
            currency="NGN",
            items=[{"name": "x"}],
            shipping={"address": "y"},
        )
        method, url, kw = last()
        assert method == "POST" and url.endswith("/order")
        assert kw["json"]["currency"] == "NGN"

    def test_list_maps_dates(self, call):
        client, last = call
        client.order.list(from_date="2026-01-01", to_date="2026-02-01", page=1)
        method, url, kw = last()
        assert method == "GET" and url.endswith("/order")
        assert kw["params"]["from"] == "2026-01-01"
        assert kw["params"]["to"] == "2026-02-01"

    def test_fetch(self, call):
        client, last = call
        client.order.fetch("ORD_1")
        _, url, _ = last()
        assert url.endswith("/order/ORD_1")

    def test_fetch_product_orders(self, call):
        client, last = call
        client.order.fetch_product_orders("PROD_1")
        _, url, _ = last()
        assert url.endswith("/order/product/PROD_1")

    def test_validate(self, call):
        client, last = call
        client.order.validate("CODE_1")
        _, url, _ = last()
        assert url.endswith("/order/CODE_1/validate")


# --------------------------------------------------------------------------- #
# Storefront
# --------------------------------------------------------------------------- #
class TestStorefront:
    def test_create(self, call):
        client, last = call
        client.storefront.create(name="Shop", slug="shop", currency="NGN")
        method, url, kw = last()
        assert method == "POST" and url.endswith("/storefront")
        assert kw["json"]["slug"] == "shop"

    def test_list(self, call):
        client, last = call
        client.storefront.list(page=1)
        _, url, _ = last()
        assert url.endswith("/storefront")

    def test_update(self, call):
        client, last = call
        client.storefront.update("SF_1", name="New")
        method, url, _ = last()
        assert method == "PUT" and url.endswith("/storefront/SF_1")

    def test_delete(self, call):
        client, last = call
        client.storefront.delete("SF_1")
        method, url, _ = last()
        assert method == "DELETE" and url.endswith("/storefront/SF_1")

    def test_verify_slug(self, call):
        client, last = call
        client.storefront.verify_slug("shop")
        _, url, _ = last()
        assert url.endswith("/storefront/verify/shop")

    def test_add_products(self, call):
        client, last = call
        client.storefront.add_products("SF_1", [1, 2])
        method, url, kw = last()
        assert method == "POST" and url.endswith("/storefront/SF_1/product")
        assert kw["json"] == {"products": [1, 2]}

    def test_publish(self, call):
        client, last = call
        client.storefront.publish("SF_1")
        method, url, _ = last()
        assert method == "POST" and url.endswith("/storefront/SF_1/publish")

    def test_duplicate(self, call):
        client, last = call
        client.storefront.duplicate("SF_1")
        method, url, _ = last()
        assert method == "POST" and url.endswith("/storefront/SF_1/duplicate")


# --------------------------------------------------------------------------- #
# Customer authorizations + direct debit
# --------------------------------------------------------------------------- #
class TestCustomerAuthorizations:
    def test_initialize_authorization(self, call):
        client, last = call
        client.customers.initialize_authorization(email="a@b.com", channel="direct_debit")
        method, url, kw = last()
        assert method == "POST" and url.endswith("/customer/authorization/initialize")
        assert kw["json"]["channel"] == "direct_debit"

    def test_verify_authorization(self, call):
        client, last = call
        client.customers.verify_authorization("ref_1")
        _, url, _ = last()
        assert url.endswith("/customer/authorization/verify/ref_1")

    def test_deactivate_authorization_uses_spec_path(self, call):
        client, last = call
        client.customers.deactivate_authorization("AUTH_1")
        method, url, _ = last()
        assert method == "POST" and url.endswith("/customer/authorization/deactivate")

    def test_initialize_direct_debit(self, call):
        client, last = call
        client.customers.initialize_direct_debit(
            "CUS_1",
            account={"number": "1"},
            address={"street": "x"},
        )
        method, url, _ = last()
        assert method == "POST" and url.endswith("/customer/CUS_1/initialize-direct-debit")

    def test_directdebit_activation_charge(self, call):
        client, last = call
        client.customers.directdebit_activation_charge("CUS_1", "AUTH_1")
        method, url, kw = last()
        assert method == "PUT" and url.endswith("/customer/CUS_1/directdebit-activation-charge")
        assert kw["json"] == {"authorization_id": "AUTH_1"}

    def test_fetch_mandate_authorizations(self, call):
        client, last = call
        client.customers.fetch_mandate_authorizations("CUS_1")
        _, url, _ = last()
        assert url.endswith("/customer/CUS_1/directdebit-mandate-authorizations")


# --------------------------------------------------------------------------- #
# Missing single endpoints
# --------------------------------------------------------------------------- #
class TestMissingSingletons:
    def test_product_delete(self, call):
        client, last = call
        client.products.delete("PROD_1")
        method, url, _ = last()
        assert method == "DELETE" and url.endswith("/product/PROD_1")

    def test_refund_retry(self, call):
        client, last = call
        client.refunds.retry_with_customer_details("RF_1", {"account_number": "1"})
        method, url, kw = last()
        assert method == "POST" and url.endswith("/refund/retry_with_customer_details/RF_1")
        assert "refund_account_details" in kw["json"]

    def test_transfer_export(self, call):
        client, last = call
        client.transfers.export(status="success", from_date="2026-01-01", to_date="2026-02-01")
        method, url, kw = last()
        assert method == "GET" and url.endswith("/transfer/export")
        assert kw["params"]["from"] == "2026-01-01"

    def test_dva_assign(self, call):
        client, last = call
        client.dedicated_accounts.assign(
            email="a@b.com",
            first_name="A",
            last_name="B",
            phone="+234",
            preferred_bank="wema-bank",
            country="NG",
        )
        method, url, _ = last()
        assert method == "POST" and url.endswith("/dedicated_account/assign")

    def test_balance_ledger_pagination(self, call):
        client, last = call
        client.transfer_control.fetch_balance_ledger(per_page=10, page=2)
        method, url, kw = last()
        assert method == "GET" and url.endswith("/balance/ledger")
        assert kw["params"]["perPage"] == 10
        assert kw["params"]["page"] == 2
