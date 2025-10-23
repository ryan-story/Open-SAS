#!/bin/bash
# Upload Open-SAS v0.1.1 to PyPI

set -e

echo "======================================"
echo "Open-SAS v0.1.1 - PyPI Upload Script"
echo "======================================"
echo ""

# Check if distribution files exist
if [ ! -f "dist/open_sas-0.1.1-py3-none-any.whl" ]; then
    echo "❌ Error: Distribution files not found!"
    echo "Please run: python setup.py sdist bdist_wheel"
    exit 1
fi

echo "✅ Distribution files found:"
ls -lh dist/open_sas-0.1.1*
echo ""

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "❌ Error: twine is not installed!"
    echo "Please run: pip install twine"
    exit 1
fi

echo "✅ twine is installed"
echo ""

# Check for PyPI credentials
if [ -f .pypirc ]; then
    echo "✅ Found local .pypirc configuration"
    echo ""
    echo "Uploading to PyPI..."
    twine upload --config-file .pypirc dist/open_sas-0.1.1*
elif [ -f ~/.pypirc ]; then
    echo "✅ Found ~/.pypirc configuration"
    echo ""
    echo "Uploading to PyPI..."
    twine upload dist/open_sas-0.1.1*
else
    echo "⚠️  No .pypirc found"
    echo ""
    echo "You'll need to enter your PyPI API token."
    echo "Get it from: https://pypi.org/manage/account/token/"
    echo ""
    echo "When prompted:"
    echo "  Username: __token__"
    echo "  Password: pypi-AgEI... (your token)"
    echo ""
    read -p "Press Enter to continue..."
    twine upload dist/open_sas-0.1.1*
fi

echo ""
echo "======================================"
echo "✅ Upload complete!"
echo "======================================"
echo ""
echo "Verify at: https://pypi.org/project/open-sas/"
echo ""
echo "Test installation:"
echo "  pip install --upgrade open-sas"
echo "  python -c \"import open_sas; print(open_sas.__version__)\""
echo ""
echo "Next steps:"
echo "  1. Create GitHub release: git tag -a v0.1.1 -m 'Release v0.1.1'"
echo "  2. Push tag: git push origin v0.1.1"
echo "  3. Create release on GitHub with CHANGELOG notes"
echo ""

