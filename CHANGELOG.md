# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-13

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

## [1.0.0] - 2024-02-13

### Added

- Initial release: Django integration for the Paystack payment gateway with
  API clients, models, webhook handling, signals, and management commands.
