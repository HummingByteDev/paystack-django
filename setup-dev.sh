#!/bin/bash
# Django Paystack Development Setup Script

set -e

echo "🚀 Setting up Django Paystack development environment..."

# Check Python version
python_version=$(python --version | cut -d' ' -f2)
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install development dependencies
echo "📥 Installing dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pip install pre-commit
pre-commit install || true

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your Paystack credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your Paystack credentials"
echo "2. Run: pip install -e '.[dev]'"
echo "3. Run tests: pytest"
echo "4. Start development: python manage.py runserver"
echo ""
echo "For more information, see INSTALLATION.md"
