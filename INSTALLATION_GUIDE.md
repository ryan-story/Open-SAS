# Open-SAS Installation Guide (v0.1.1)

## Critical Bug Fixes in v0.1.1

This version fixes critical dependency issues that prevented the Jupyter kernel from installing properly on Windows and other systems.

### What Was Fixed:
- **Issue #1**: `ModuleNotFoundError: No module named 'ipykernel'` - The `ipykernel` and `jupyter` packages are now included as required dependencies instead of optional ones.
- **Issue #2**: Package detection issues - Improved error messages and installation process.

## Installation Instructions

### For Your Friend on Windows (Python 3.13)

#### Step 1: Uninstall Old Version (if installed)
```powershell
pip uninstall open-sas -y
```

#### Step 2: Install the New Version

**Option A: Install from the wheel file (recommended)**
```powershell
pip install path\to\open_sas-0.1.1-py3-none-any.whl
```

**Option B: Install from source**
```powershell
pip install path\to\open_sas-0.1.1.tar.gz
```

#### Step 3: Install the Jupyter Kernel
```powershell
python -m open_sas.kernel install
```

This should now work without the `ipykernel` error!

#### Step 4: Verify Installation
```powershell
# Check package version
python -c "import open_sas; print(open_sas.__version__)"

# Check kernel installation
jupyter kernelspec list
```

You should see `osas` in the list of available kernels.

### Running .osas Files

#### Option 1: Using the Command Line Tool
```powershell
open-sas path\to\your\file.osas
```

#### Option 2: Using Python Directly
```powershell
python -m open_sas path\to\your\file.osas
```

#### Option 3: Using the VS Code Extension

If you're using the VS Code extension for Open-SAS, make sure:
1. The package is properly installed: `pip show open-sas`
2. The Python interpreter in VS Code matches where you installed the package
3. You can verify the Python path with: `where python` (Windows) or `which python` (Mac/Linux)

### About PROC SQL with ODBC

The code your friend wrote uses PROC SQL with ODBC connections:

```sas
proc sql;
connect to odbc (dsn='OwlConnectLive' user='wd2' password='xxxxxxxx');
create table comment as
  select *
   from connection to odbc(
SELECT *
  FROM [OwlConnect_Prod].[dbo].[V_QUERY_GROUPMEMBERDATERANGE]);
quit;
```

**Important Note**: Open-SAS currently supports basic PROC SQL functionality but **does not yet support ODBC pass-through connections**. The `CONNECT TO ODBC` syntax is a feature that would need to be added.

For now, if you need to work with external databases:

1. **Use Python libraries directly** with pandas:
   ```python
   import pyodbc
   import pandas as pd
   
   conn = pyodbc.connect('DSN=OwlConnectLive;UID=wd2;PWD=xxxxxxxx')
   df = pd.read_sql("SELECT * FROM [OwlConnect_Prod].[dbo].[V_QUERY_GROUPMEMBERDATERANGE]", conn)
   # Then use Open-SAS for subsequent analysis
   ```

2. **Export data first**, then use Open-SAS for analysis

## Troubleshooting

### "Package not found" Error

If you still see "ERROR: Open-SAS package not found":

1. **Check Python installation location**:
   ```powershell
   where python
   pip show open-sas
   ```

2. **Make sure you're using the same Python**:
   - The Python you used to install should be the same one executing the code
   - VS Code might use a different Python interpreter

3. **Try installing in user mode**:
   ```powershell
   pip install --user open_sas-0.1.1-py3-none-any.whl
   ```

### Import Errors After Installation

If you get import errors:
```powershell
# Reinstall with all dependencies
pip install --force-reinstall open_sas-0.1.1-py3-none-any.whl
```

### Jupyter Kernel Issues

If the kernel doesn't show up in Jupyter:

1. **Check kernel installation location**:
   ```powershell
   jupyter kernelspec list
   ```

2. **Reinstall the kernel**:
   ```powershell
   python -m open_sas.kernel uninstall
   python -m open_sas.kernel install
   ```

3. **Restart Jupyter**:
   - Close all Jupyter instances
   - Restart your terminal
   - Start Jupyter again

## What's New in v0.1.1

### Dependencies Now Included
- `jupyter>=1.0.0`
- `ipykernel>=6.0.0`

These were previously optional but are now required since the kernel is a core feature.

### Python Version Support
- Added official support for Python 3.12 and 3.13
- Maintains compatibility with Python 3.8+

## Getting Help

If you encounter issues:

1. **Check the version**: `python -c "import open_sas; print(open_sas.__version__)"` should show `0.1.1`
2. **Verify all dependencies**: `pip check`
3. **Check kernel status**: `jupyter kernelspec list`

For more examples and documentation, see:
- `examples/osas_walkthrough.ipynb` - Comprehensive feature walkthrough
- `examples/ML_project_in_osas.ipynb` - Machine learning examples
- `README.md` - Project overview and quick start

## Contact

For bug reports or feature requests, please visit the GitHub repository.

