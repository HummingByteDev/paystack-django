# Contributing to paystack-django

Thank you for your interest in contributing to paystack-django! We welcome contributions from anyone and are grateful for even the smallest of fixes!

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, search the issue list to see if the problem has already been reported. If you find your bug is not listed, create a new issue with:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem** in as many details as possible
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** after following the steps
- **Explain which behavior you expected to see** instead and why
- **Include screenshots and animated GIFs** if possible
- **Include your environment details**:
  - Python version
  - Django version
  - paystack-django version
  - Operating System

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, provide:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and **the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

Pull requests are the best way to propose changes. We actively welcome them.

- Fill in the provided pull request template
- Follow the Python/Django styleguides
- Document new code with docstrings
- End all files with a newline
- Avoid platform-dependent code
- Add tests for any new functionality

## Development Setup

### 1. Fork and Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/django-paystack.git
cd django-paystack
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Create a New Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=djpaystack --cov-report=html

# Run specific test file
pytest djpaystack/tests/test_client.py

# Run specific test
pytest djpaystack/tests/test_client.py::TestPaystackClient::test_initialization
```

### Running Tests Across Python Versions

```bash
tox
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code with black
black djpaystack

# Sort imports with isort
isort djpaystack

# Check for style issues
flake8 djpaystack

# Run type checks
mypy djpaystack
```

### Automated Code Quality

Before submitting a pull request, run all checks:

```bash
# Format and check
black djpaystack
isort djpaystack
flake8 djpaystack
mypy djpaystack --ignore-missing-imports
pytest --cov=djpaystack
```

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐛 `:bug:` when fixing a bug
  - ✅ `:white_check_mark:` when adding tests
  - 📚 `:books:` when writing docs
  - 🎉 `:tada:` when releasing a new version
  - ⚡ `:zap:` when improving performance
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies

Example:

```
🎨 Reformat payment response handling

- Improved clarity of response parsing
- Added inline documentation
- Fixes #123
```

### Python Styleguide

We follow PEP 8 with the following additions:

- Use type hints for function parameters and return values
- Maximum line length is 100 characters (not 79)
- Use docstrings for all public modules, functions, classes, and methods
- Use Google-style docstrings

Example:

```python
def initialize_transaction(
    email: str,
    amount: int,
    reference: str,
    **kwargs
) -> Dict[str, Any]:
    """
    Initialize a new transaction on Paystack.

    Args:
        email: Customer email address
        amount: Amount in kobo (e.g., 50000 = 500 NGN)
        reference: Unique transaction reference

    Returns:
        API response containing authorization URL and access code

    Raises:
        PaystackValidationError: If validation fails
        PaystackAPIError: If API returns an error
    """
```

### Documentation Styleguide

- Use Markdown for documentation
- Use clear, concise language
- Include code examples where helpful
- Update relevant documentation when making changes

## Pull Request Process

1. **Create a fork** of the repository
2. **Create a feature branch** from `main`
3. **Make your changes** with clear, descriptive commits
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Run tests** and ensure they pass
7. **Push to your fork** and create a Pull Request
8. **Write a clear PR description** explaining your changes
9. **Link any related issues** using keywords like `Closes #123`

## What to Include in a Pull Request

- **Clear description** of the changes made
- **Link to related issues** (if applicable)
- **Testing information**: What tests did you run? How did you verify?
- **Screenshots or examples** (if visual changes)
- **Backward compatibility** notes (if applicable)
- **Performance impact** (if applicable)

## Review Process

- At least one maintainer review is required before merging
- Automated tests must pass
- Code quality checks must pass
- Documentation must be updated

## Release Process

1. Update `__version__` in `djpaystack/__init__.py`
2. Update `pyproject.toml` version
3. Update `CHANGELOG.md` with release notes
4. Create a new Git tag: `git tag v1.x.x`
5. Push to repository
6. Build and upload to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Dependencies

When adding new dependencies:

1. Consider the impact on package size and installation time
2. Use well-maintained, popular packages
3. Add to appropriate section in `pyproject.toml`
4. Update documentation with new dependency information
5. Explain why the dependency is needed in the PR

## Questions?

Feel free to ask questions by:

- Opening an issue with the `question` label
- Starting a discussion on GitHub Discussions
- Emailing the maintainers

## Additional Notes

- This is a volunteer-driven project
- We appreciate your patience as maintainers may need time to review
- Be respectful to other contributors
- Help others when you can

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

---

**Thank you for contributing to paystack-django!** 🎉
