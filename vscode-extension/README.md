# Open-SAS VS Code Extension

<div align="center">
  <img src="../media/osas.png" alt="Open-SAS Logo" width="100">
  <h3>Statistical analysis syntax highlighting and execution support for VS Code</h3>
  <p><em>SAS® is a registered trademark of SAS Institute Inc. Open-SAS is not affiliated with, endorsed by, or sponsored by SAS Institute Inc.</em></p>
</div>

## Features

- **Syntax Highlighting**: Full statistical analysis syntax highlighting for `.osas` and `.sas` files
- **Code Snippets**: Common statistical analysis patterns and procedures
- **File Execution**: Run Open-SAS files directly from VS Code
- **Notebook Support**: Interactive statistical notebooks (both `.ipynb` with osas kernel and `.osasnb` files)
- **IntelliSense**: Code completion and syntax checking
- **Integrated Terminal**: View results in VS Code's integrated terminal

## Installation

1. Install the extension from the VS Code Marketplace
2. Install the Open-SAS Python package:
   ```bash
   pip install open-sas
   ```
3. Install the Jupyter kernel (optional, for notebook support):
   ```bash
   python -m open_sas.kernel install
   ```

## Usage

### Basic SAS Files (.osas)
1. Create a new file with `.osas` extension
2. Write your SAS code
3. Use `Ctrl+Shift+P` → "Open-SAS: Run File" to execute
4. View results in the integrated terminal

### Interactive Notebooks
**Option 1: Standard Jupyter Notebooks (.ipynb)**
1. Install the Open-SAS kernel: `python -m open_sas.kernel install`
2. Create a new Jupyter notebook (`.ipynb`)
3. Select "osas" as the kernel
4. Write SAS code in cells and execute

**Option 2: Open-SAS Notebooks (.osasnb)**
1. Create a new file with `.osasnb` extension
2. Write SAS code in cells
3. Execute cells individually or run all
4. View formatted output and datasets

### Code Snippets
Type common statistical analysis patterns and press `Tab` to expand:
- `data` → DATA step template
- `proc` → Statistical procedure template
- `means` → PROC MEANS template
- `freq` → PROC FREQ template

## Supported Features

- **DATA Steps**: Variable creation, conditional logic, DATALINES
- **PROC MEANS**: Descriptive statistics with CLASS variables
- **PROC FREQ**: Frequency tables and cross-tabulations
- **PROC SORT**: Data sorting with ascending/descending order
- **PROC PRINT**: Data display and formatting
- **Macro Variables**: %LET, %PUT statements
- **Libraries**: LIBNAME functionality

## Configuration

The extension can be configured through VS Code settings:

- `open-sas.pythonPath`: Path to Python executable
- `open-sas.openSASPath`: Path to Open-SAS runner script
- `open-sas.showOutputOnRun`: Show output channel when running code

## Requirements

- Python 3.8 or higher
- Open-SAS Python package
- VS Code 1.60.0 or higher

## Demo

Check out the comprehensive demo in `examples/osas_walkthrough.ipynb` to see all features in action.

## Contributing

Contributions are welcome! Please see the [main project repository](https://github.com/ryan-story/Open-SAS) for contribution guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Support

- 📖 [Documentation](https://github.com/ryan-story/Open-SAS/wiki)
- 🐛 [Issue Tracker](https://github.com/ryan-story/Open-SAS/issues)
- 💬 [Discussions](https://github.com/ryan-story/Open-SAS/discussions)
