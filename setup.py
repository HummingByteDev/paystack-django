"""
Setup configuration for paystack-django
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paystack-django",
    version="1.0.0",
    author="Humming Byte",
    author_email="contact@hummingbyte.com",
    description="A comprehensive Django integration for Paystack Payment Gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HummingByteDev/paystack-django",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "requests>=2.25.0",
        "urllib3>=1.26.0",
        "python-decouple>=3.5",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-django>=4.5",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "isort>=5.10",
            "mypy>=0.950",
            "django-stubs>=1.12.0",
            "tox>=3.24",
        ],
        "docs": [
            "sphinx>=4.5",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.18",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "django",
        "paystack",
        "payment",
        "payment-gateway",
        "nigerian-payment",
    ],
)
