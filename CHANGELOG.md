# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-06-20

### Security

- **Fixed webhook signature bypass** — `verify_signature()` now returns `False` (instead of `True`) when `WEBHOOK_SECRET` is not configured, preventing unsigned payloads from being accepted.
- **Fixed `naira_to_kobo` floating-point precision** — Changed from `int(naira * 100)` to `int(Decimal(str(naira)) * 100)` to prevent rounding errors on real currency amounts.
- **Webhook IP verification** — `_get_client_ip()` now correctly resolves client IPs from `X-Forwarded-For` headers and the IP whitelist check is actually invoked.

### Added

- **Charge API** — Added `bank_transfer`, `eft`, and `qr` parameters to `ChargeAPI.create()` for Pay with Transfer, EFT (South Africa / Ozow), and QR code (scan-to-pay) payment channels.
- **Transaction API** — Added `split` parameter (dict) to `TransactionAPI.initialize()` for on-the-fly dynamic split configuration; added `split_code` and `callback_url` to `charge_authorization()`.
- **Dedicated Account API** — Added `DedicatedAccountAPI.assign()` for single-step Dedicated Virtual Account creation; fixed `split()` to accept `account_number` instead of `customer`; added `date` parameter to `requery()`.
- **Refund API** — Added `RefundAPI.retry()` for retrying refunds stuck in `refund.needs-attention` status.
- **Webhook events** — Added `BANK_TRANSFER_REJECTED`, `REFUND_PROCESSING`, `REFUND_NEEDS_ATTENTION`, `DIRECT_DEBIT_AUTHORIZATION_CREATED`, and `DIRECT_DEBIT_AUTHORIZATION_ACTIVE` events to the `WebhookEvent` enum.
- **Context manager** — `PaystackClient` now supports `with` statements (`__enter__` / `__exit__`) for automatic session cleanup.
- **System checks** — Django system checks now raise `E001` for a missing `SECRET_KEY` and `W001` for a missing `WEBHOOK_SECRET`.
- **`PaystackCallbackView`** — A class-based callback view (`djpaystack.views`) to handle Paystack redirect callbacks.
- **New tests** — Added `test_middleware.py`, `test_decorators.py`, `test_settings.py`, `test_admin.py`, `test_views.py`, and `test_webhook_security.py` — test suite grew from 27 to 64 tests.

### Changed

- **Direct Debit API** — Complete rewrite replacing fabricated `/mandate/` endpoints with the correct Paystack endpoints: `initialize_authorization`, `verify_authorization`, `activation_charge`, and `bulk_activation_charge`.
- **Dispute webhook events** — Renamed `DISPUTE_CREATE` / `DISPUTE_RESOLVE` to `CHARGE_DISPUTE_CREATE` / `CHARGE_DISPUTE_RESOLVE` to match Paystack's actual `charge.dispute.*` event names.
- **Logging** — Replaced f-string logging calls with lazy `%s` formatting throughout the codebase (`client.py`, `middleware.py`, `handlers.py`, `decorators.py`).
- **Removed `python-decouple` dependency** — The package no longer requires `python-decouple`; use `os.environ` or any config loader of your choice.

### Removed

- **Deprecated `default_app_config`** — Removed from `djpaystack/__init__.py` (unnecessary since Django 3.2+).
- **`setup.cfg`** — Consolidated all metadata into `pyproject.toml` as the single source of truth.
- **Redundant database indexes** — Migration `0002_remove_redundant_indexes` removes duplicate indexes that were already covered by `unique=True` and `db_index=True`.

### Fixed

- **Webhook handler deduplication** — Switched from `set()` to `OrderedDict` for processed-event tracking to ensure FIFO eviction and deterministic behaviour.
- **Admin test configuration** — Added `django.contrib.admin`, `sessions`, and `messages` to test `INSTALLED_APPS` so admin tests run correctly.

---

## [1.0.0] - 2024-02-13

### Added

- ✨ Complete Paystack API integration with all endpoints
- ✨ Django models for transactions, customers, plans, products, and more
- ✨ Webhook support with automatic verification and signal dispatch
- ✨ Comprehensive configuration system with environment variable support
- ✨ Signal support for payment events (success, failed, verified, etc.)
- ✨ Type hints throughout the codebase for better IDE support
- ✨ Extensive error handling with custom exception classes
- ✨ Automatic retry mechanism with exponential backoff
- ✨ Request/response logging for debugging
- ✨ Pagination support for list endpoints
- ✨ Caching support for frequently accessed data
- ✨ Async-ready design for future async support
- ✨ Comprehensive test suite with high coverage
- ✨ Full API documentation with examples
- ✨ Support for Django 3.2 through Django 5.0
- ✨ Support for Python 3.8 through Python 3.12

### Supported Services

- Transactions - Create, verify, and manage transactions
- Customers - Create and manage customer records
- Plans - Create and manage subscription plans
- Subscriptions - Manage customer subscriptions
- Transfers - Handle fund transfers to bank accounts
- Refunds - Process and manage refunds
- Disputes - Manage transaction disputes
- Settlements - Track settlement information
- Splits - Configure payment splits between accounts
- Subaccounts - Manage subaccounts
- Products - Create and manage products
- Payment Requests - Generate payment request links
- Verification - Bank and account verification
- Direct Debit - Direct debit authorization
- Terminal - Terminal operations
- Apple Pay - Apple Pay integration
- Virtual Terminal - Virtual terminal operations
- Pages - Create and manage pages
- Bulk Charges - Batch charge operations
- Integration - Integration-related operations
- Miscellaneous - Other utility endpoints

### Features

- 🔐 Secure webhook signature verification
- 🔄 Automatic transaction verification
- 📊 Comprehensive transaction tracking
- 🏪 Multi-merchant support via subaccounts
- 💳 Multiple payment methods support
- 📱 Apple Pay integration
- 💰 Payment splits and routing
- 🔗 Linked bank accounts for payouts
- 📧 Email-based customer identification
- 🏦 Bank account verification
- 📱 Phone number verification
- 🗂️ Flexible metadata storage
- 🔍 Advanced filtering and pagination
- 📝 Comprehensive logging

### Documentation

- 📚 Full API documentation
- 🎓 Quick start guide
- 📖 Configuration guide
- 🔧 Integration examples
- 🧪 Testing guide
- 🔐 Security best practices

---

---

## Support

For issues or feature requests, please visit [GitHub Issues](https://github.com/HummingByteDev/paystack-django/issues).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
