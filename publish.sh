#!/bin/bash
# Build and publish to PyPI

set -e

echo "🚀 Building paystack-django for PyPI..."

# Check if build tools are installed
if ! command -v python -m build &> /dev/null; then
    echo "❌ build module not found. Installing..."
    pip install build twine
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.egg-info

# Build distribution
echo "📦 Building distribution..."
python -m build

# Check distribution
echo "🔍 Checking distribution..."
python -m twine check dist/*

# Ask for environment
read -p "Publish to (test/production)? " env

if [ "$env" = "test" ]; then
    echo "📤 Publishing to TestPyPI..."
    python -m twine upload --repository testpypi dist/*
    echo "✅ Published to TestPyPI"
    echo "Install with: pip install --index-url https://test.pypi.org/simple/ paystack-django"
elif [ "$env" = "production" ]; then
    read -p "Are you sure? This cannot be undone. (yes/no) " confirm
    if [ "$confirm" = "yes" ]; then
        echo "📤 Publishing to PyPI..."
        python -m twine upload dist/*
        echo "✅ Published to PyPI"
        echo "Install with: pip install paystack-django"
    else
        echo "❌ Cancelled"
    fi
else
    echo "❌ Invalid option"
    exit 1
fi
