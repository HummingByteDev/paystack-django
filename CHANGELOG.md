# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<<<<<<< HEAD
## [2.0.0] - 2026-06-13

This is a major release: it completes Paystack API coverage and includes
behavioural **breaking changes** (see the *Breaking changes* section below).

### Added

- Clients for the full Paystack API surface, including **Virtual Terminal**,
  **Direct Debit**, **Orders**, and **Storefronts**.
- Customer authorization and direct-debit onboarding: `initialize_authorization`,
  `verify_authorization`, `initialize_direct_debit`,
  `directdebit_activation_charge`, and `fetch_mandate_authorizations`.
- Additional endpoints: product `delete`, refund `retry_with_customer_details`,
  transfer `export`, dedicated-account `assign`, and balance-ledger pagination.
- Lazy `iter_all()` iterators on `transactions` and `customers` to stream every
  record across pages with bounded memory.
- `WEBHOOK_SIGNATURE_REQUIRED` setting (defaults to `True`).

### Changed

- **`WEBHOOK_SECRET` now defaults to `SECRET_KEY`.** Paystack signs webhooks with
  the account secret key, so `WEBHOOK_SECRET` is an optional override.
- Added a `User-Agent: paystack-django/<version>` header to all requests.
- HTTP 401/403 responses now raise `PaystackAuthenticationError`.
- Webhook datetime fields (`paid_at`, `next_payment_date`, `transferred_at`) are
  parsed into real `datetime` objects.
- `sync_paystack_data` honours `--days` and iterates lazily.
- Consolidated build configuration onto `pyproject.toml`; removed `setup.py` and
  `setup.cfg`. Removed the unused `python-decouple` dependency and raised the
  `requests` floor to `>=2.32.0`.
- The package is fully formatted with black and isort, and CI now enforces
  linting, formatting, typing, coverage, and dependency/security scanning.

### Fixed

- Webhook signature verification now **fails closed** when no signing key can be
  resolved (previously it accepted unverified webhooks).
- Non-idempotent requests (`POST`/`PUT`) are no longer automatically retried,
  preventing duplicate charges/transfers on transient errors.
- Webhook deduplication is now race-safe and database-backed, so concurrent or
  redelivered webhooks are processed exactly once across multiple workers.
- List endpoints send the correct `from`/`to` date filters (were ignored).
- Dispute webhook events use their correct `charge.dispute.*` names, so dispute
  handlers and signals fire.
- Bulk-charge `pause()`/`resume()` use the correct request method and path.
- `charge.submit_address()` sends `zip_code` (was `zipcode`).
- `transfers.list()` filters by `recipient` (with `customer` kept as a
  deprecated alias).
- Transfer reversals are recorded with status `reversed` (was `failed`).
- `list()` no longer eagerly loads every page into memory; it returns a single
  page (use `iter_all()` to stream all records).

### Breaking changes

- Webhooks are rejected when no `SECRET_KEY`/`WEBHOOK_SECRET` is configured.
- `POST`/`PUT` requests are not auto-retried; retry writes yourself with a stable
  `reference`.
- `list()` returns a single page instead of all pages; use `iter_all()`.
- `setup.py`/`setup.cfg` removed in favour of `pyproject.toml`.

See the documentation for migration guidance.
=======
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
>>>>>>> 325e07c878dfd700edf7fb979eeb411197c9663f

## [1.0.0] - 2024-02-13

### Added

- Initial release: Django integration for the Paystack payment gateway with
  API clients, models, webhook handling, signals, and management commands.
