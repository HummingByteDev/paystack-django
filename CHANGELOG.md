# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
