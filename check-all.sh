#!/bin/bash
# Run all development checks

set -e

echo "🔍 Running development checks..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
FAILED=0

# Run black
echo "🎨 Checking code formatting with black..."
if black --check djpaystack 2>/dev/null; then
    echo -e "${GREEN}✓ Black check passed${NC}"
else
    echo -e "${YELLOW}⚠ Black check failed - running black...${NC}"
    black djpaystack
fi

# Run isort
echo ""
echo "📦 Checking import sorting with isort..."
if isort --check-only djpaystack 2>/dev/null; then
    echo -e "${GREEN}✓ isort check passed${NC}"
else
    echo -e "${YELLOW}⚠ isort check failed - running isort...${NC}"
    isort djpaystack
fi

# Run flake8
echo ""
echo "⚠️  Running flake8 linting..."
if flake8 djpaystack --max-line-length=100 --ignore=E203,W503; then
    echo -e "${GREEN}✓ flake8 check passed${NC}"
else
    FAILED=$((FAILED + 1))
fi

# Run mypy
echo ""
echo "🔤 Running type checking with mypy..."
if mypy djpaystack --ignore-missing-imports; then
    echo -e "${GREEN}✓ mypy check passed${NC}"
else
    echo -e "${YELLOW}⚠ mypy check had issues${NC}"
fi

# Run pytest
echo ""
echo "🧪 Running pytest..."
if pytest --cov=djpaystack --cov-report=term-missing; then
    echo -e "${GREEN}✓ Tests passed${NC}"
else
    FAILED=$((FAILED + 1))
fi

echo ""
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
else
    echo -e "${RED}❌ Some checks failed${NC}"
    exit 1
fi
