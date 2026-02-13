.. _contributing:

Contributing
============

Thank you for considering contributing to paystack-django! We welcome contributions from the community.

Getting Started
---------------

1. Fork the repository
2. Clone your fork: ``git clone https://github.com/yourusername/paystack-django.git``
3. Create a branch: ``git checkout -b feature-name``
4. Install development dependencies: ``pip install -e ".[dev]"``

.. code-block:: bash

    cd paystack-django
    pip install -e ".[dev]"
    pre-commit install

Code Style
----------

We use the following tools:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run checks:

.. code-block:: bash

    make lint
    make format
    make type-check

Testing
-------

Write tests for your changes:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=djpaystack

    # Run specific test
    pytest djpaystack/tests/test_transactions.py

Documentation
-------------

Update documentation for new features:

.. code-block:: bash

    cd docs
    make html
    # Open _build/html/index.html

Commit Messages
---------------

Use clear commit messages:

.. code-block:: bash

    git commit -m "Add feature X

    - Brief description of changes
    - Additional details if needed
    "

Pull Request Process
--------------------

1. Update CHANGELOG.md
2. Add tests for new features
3. Update documentation
4. Submit PR with clear description
5. Ensure all checks pass

Code of Conduct
---------------

Be respectful and inclusive. We're all here to learn and help.

Questions?
----------

- Open an issue on GitHub
- Start a discussion
- Email: dev@hummingbyte.org

Thank you for contributing! 🎉
