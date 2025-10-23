# PyPI Release Guide for Open-SAS v0.1.1

## Prerequisites

Before releasing to PyPI, ensure you have:

1. **PyPI Account**: Sign up at https://pypi.org if you don't have one
2. **API Token**: Create one at https://pypi.org/manage/account/token/
3. **Twine Installed**: Already installed (`/opt/anaconda3/bin/twine`)

## Quick Release (Recommended)

### Step 1: Set up PyPI API Token

Create a `~/.pypirc` file with your API token:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC... # Your API token here
```

**Important**: Replace with your actual API token from https://pypi.org/manage/account/token/

Make sure the file has proper permissions:
```bash
chmod 600 ~/.pypirc
```

### Step 2: Upload to PyPI

```bash
cd "/Users/rs255/My Technologies/Open-SAS"
twine upload dist/open_sas-0.1.1*
```

That's it! The package will be available at https://pypi.org/project/open-sas/

## Alternative: Manual Token Entry

If you prefer not to save the token:

```bash
cd "/Users/rs255/My Technologies/Open-SAS"
twine upload dist/open_sas-0.1.1*
```

When prompted:
- Enter your API token: `pypi-AgEIcHlwaS5vcmcC...`

## Verify the Upload

After upload, verify at:
- Project page: https://pypi.org/project/open-sas/
- Version page: https://pypi.org/project/open-sas/0.1.1/

## Test the Installation

```bash
# In a fresh environment
pip install --upgrade open-sas

# Verify version
python -c "import open_sas; print(open_sas.__version__)"
# Should print: 0.1.1

# Test kernel installation
python -m open_sas.kernel install
jupyter kernelspec list
# Should show 'osas' in the list
```

## What Gets Uploaded

The following files will be uploaded:
- `dist/open_sas-0.1.1-py3-none-any.whl` (101KB) - Universal wheel
- `dist/open_sas-0.1.1.tar.gz` (79KB) - Source distribution

## Troubleshooting

### Issue: "File already exists"

If you've already uploaded this version:
- Increment the version number in `setup.py` to `0.1.2`
- Update all version references
- Rebuild: `python setup.py sdist bdist_wheel`
- Upload again

### Issue: "Invalid credentials"

- Verify your API token is correct
- Make sure you're using `__token__` as the username
- Check that your token has upload permissions

### Issue: "Package name already taken"

The package name `open-sas` should already be registered to you. If not:
- You may need to request access
- Or use a different package name (e.g., `open-sas-ryan`)

## Post-Release Checklist

After successful PyPI release:

- [ ] Verify installation: `pip install --upgrade open-sas`
- [ ] Test kernel: `python -m open_sas.kernel install`
- [ ] Update GitHub release notes
- [ ] Tag the release: `git tag v0.1.1 && git push origin v0.1.1`
- [ ] Send updated wheel to your friend
- [ ] Update VS Code extension marketplace (if needed)
- [ ] Announce on social media / forums (optional)

## GitHub Release

Create a GitHub release to match:

```bash
git tag -a v0.1.1 -m "Release v0.1.1: Critical dependency fixes"
git push origin v0.1.1
```

Then go to https://github.com/ryan-story/Open-SAS/releases/new and:
1. Select tag `v0.1.1`
2. Title: `Open-SAS v0.1.1 - Critical Dependency Fixes`
3. Description: Copy from CHANGELOG.md
4. Attach: `dist/open_sas-0.1.1-py3-none-any.whl`
5. Attach: `dist/open_sas-0.1.1.tar.gz`

## VS Code Extension Update

The VS Code extension has been updated to v0.2.1 with:
- Updated README to reflect automatic kernel dependency installation
- Version bump in package.json

To publish the extension update:

```bash
cd vscode-extension
npm install -g vsce  # If not already installed
vsce package
vsce publish
```

You'll need your VS Code Marketplace publisher token.

## Summary of Changes in v0.1.1

### Critical Fixes
- ✅ Moved `ipykernel>=6.0.0` to required dependencies
- ✅ Moved `jupyter>=1.0.0` to required dependencies
- ✅ Added Python 3.12 and 3.13 support

### Files Changed
- ✅ `setup.py` - Dependencies and version
- ✅ `open_sas/__init__.py` - Version
- ✅ `open_sas/kernel/osas_kernel.py` - Version
- ✅ `open_sas/kernel/working_kernel.py` - Version
- ✅ `open_sas/cli.py` - Version
- ✅ `CHANGELOG.md` - Release notes
- ✅ `vscode-extension/package.json` - Version 0.2.1
- ✅ `vscode-extension/README.md` - Updated installation instructions

### Documentation Created
- ✅ `INSTALLATION_GUIDE.md` - User installation guide
- ✅ `RESPONSE_TO_FRIEND.md` - Email template
- ✅ `BUGFIX_SUMMARY.md` - Technical changes
- ✅ `PYPI_RELEASE_GUIDE.md` - This file

## Need Help?

If you encounter any issues during the PyPI release:
1. Check PyPI status: https://status.python.org/
2. Verify twine version: `twine --version`
3. Test upload to TestPyPI first (optional):
   ```bash
   twine upload --repository testpypi dist/open_sas-0.1.1*
   ```

## Quick Command Reference

```bash
# From the project root directory
cd "/Users/rs255/My Technologies/Open-SAS"

# Upload to PyPI
twine upload dist/open_sas-0.1.1*

# Create git tag
git tag -a v0.1.1 -m "Release v0.1.1: Critical dependency fixes"
git push origin v0.1.1

# Test installation
pip install --upgrade open-sas
python -c "import open_sas; print(open_sas.__version__)"
```

---

**Ready to release!** Just run `twine upload dist/open_sas-0.1.1*` and enter your PyPI API token when prompted.

