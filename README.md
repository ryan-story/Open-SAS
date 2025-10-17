# Open-SAS

<div align="center">
  <img src="media/osas.png" alt="Open-SAS Logo" width="200">
  <h3>An open-source, Python-based statistical analysis system</h3>
  <p>Write SAS-like code with full syntax highlighting and Python backend execution.</p>
  <p><em>SAS® is a registered trademark of SAS Institute Inc. Open-SAS is not affiliated with, endorsed by, or sponsored by SAS Institute Inc.</em></p>
</div>

## Overview

Open-SAS provides an open-source alternative for statistical analysis by offering:
- **SAS-inspired syntax** for data manipulation and analysis
- **Python backend** for execution and performance
- **Jupyter notebook support** with Open-SAS kernel
- **VS Code extension** with syntax highlighting and execution
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Open source** and free to use

## Features

### Core Interpreter
- SAS-inspired DATA step functionality with DATALINES support
- Statistical procedures (PROC MEANS, PROC FREQ, PROC SORT, PROC PRINT)
- SAS-like data manipulation and analysis syntax
- Python pandas/numpy backend for performance
- Clean, professional output with familiar formatting

### Jupyter Notebook Support
- Open-SAS kernel for Jupyter notebooks
- Interactive statistical programming in notebook environment
- Rich output display with formatted tables
- Dataset visualization and exploration

### VS Code Extension
- Syntax highlighting for `.osas` and `.sas` files
- Code snippets for common statistical analysis patterns
- File execution directly from VS Code
- Notebook support for interactive analysis

### Supported Features
- **DATA Steps**: Variable creation, conditional logic, DATALINES input
- **PROC MEANS**: Descriptive statistics with CLASS variables and OUTPUT statements
- **PROC FREQ**: Frequency tables and cross-tabulations with options
- **PROC SORT**: Data sorting with ascending/descending order
- **PROC PRINT**: Data display and formatting
- **PROC REG**: Linear regression analysis with MODEL, OUTPUT, and SCORE statements
- **PROC SURVEYSELECT**: Random sampling with SRS method, SAMPRATE/N options, and OUTALL flag
- **Macro variables**: %LET, %PUT statements
- **Libraries**: LIBNAME functionality
- **NOPRINT option**: Silent execution for procedures

## Installation

### Python Package
```bash
pip install open-sas
```

### Jupyter Kernel Installation
```bash
# Install the Open-SAS kernel
python -m open_sas.kernel install

# List available kernels
jupyter kernelspec list
```

### VS Code Extension
1. Install from VS Code Marketplace: "Open-SAS" by RyanBlakeStory
2. Or install from source (see Development section)

## Quick Start

### 1. Interactive Python Usage
```python
from open_sas import SASInterpreter

# Create interpreter
interpreter = SASInterpreter()

# Create sample data using SAS-inspired syntax
interpreter.run_code('''
data work.employees;
    input employee_id name $ department $ salary;
    datalines;
1 Alice Engineering 75000
2 Bob Marketing 55000
3 Carol Engineering 80000
4 David Sales 45000
;
run;
''')

# Run statistical analysis
interpreter.run_code('''
proc means data=work.employees;
    class department;
    var salary;
run;
''')
```

### 2. Jupyter Notebook Usage
1. Install the Open-SAS kernel:
   ```bash
   python -m open_sas.kernel install
   ```
2. Create a new Jupyter notebook (`.ipynb`)
3. Select "osas" as the kernel
4. Write SAS code in cells and execute

### 3. VS Code Usage
1. Install the Open-SAS extension from the marketplace
2. Create a new file with `.osas` extension
3. Write your SAS code
4. Use `Ctrl+Shift+P` → "Open-SAS: Run File" to execute

### 4. Command Line Usage
```bash
# Run SAS code from file
python -m open_sas.cli run example.osas

# Interactive mode
python -m open_sas.cli interactive
```

## Demo

Check out `examples/osas_walkthrough.ipynb` for a comprehensive demonstration of Open-SAS capabilities including:
- DATA step with DATALINES
- Statistical procedures with CLASS variables and OUTPUT statements
- Frequency analysis with cross-tabulations
- Data sorting with ascending/descending order
- Data display and formatting
- Silent execution options

## Project Structure

```
Open-SAS/
├── open_sas/                 # Core Python package
│   ├── __init__.py
│   ├── interpreter.py        # Main statistical interpreter
│   ├── cli.py               # Command line interface
│   ├── kernel/              # Jupyter kernel implementation
│   │   ├── osas_kernel.py   # Main kernel
│   │   └── install.py       # Kernel installation
│   ├── parser/              # Syntax parser
│   │   ├── data_step_parser.py
│   │   ├── proc_parser.py
│   │   └── macro_parser.py
│   ├── procs/               # Statistical procedure implementations
│   │   ├── proc_means.py
│   │   ├── proc_freq.py
│   │   ├── proc_sort.py
│   │   └── proc_print.py
│   └── utils/               # Utility functions
│       ├── expression_evaluator.py
│       ├── data_utils.py
│       └── libname_manager.py
├── vscode-extension/         # VS Code extension
├── examples/                # Example files and demo notebook
├── media/                   # Logo and icons
├── setup.py                 # Package setup
└── README.md
```

## Development

### Setup Development Environment
```bash
git clone https://github.com/ryan-story/Open-SAS.git
cd Open-SAS
pip install -e .
```

### Running Tests
```bash
# Run basic functionality tests
python -c "from open_sas import SASInterpreter; print('Open-SAS loaded successfully')"
```

## Key Features Implemented

### ✅ Completed Features
- [x] Core DATA step implementation with DATALINES
- [x] Statistical procedures with CLASS variables and OUTPUT statements
- [x] Frequency analysis with cross-tabulations and options
- [x] Data sorting with ascending/descending order
- [x] Data display and formatting
- [x] Linear regression analysis with PROC REG
- [x] Random sampling with PROC SURVEYSELECT
- [x] Silent execution options
- [x] Jupyter notebook kernel
- [x] VS Code extension with syntax highlighting
- [x] Clean, professional output
- [x] SAS-inspired behavior and syntax

### 🚧 Future Enhancements
- [ ] Additional statistical procedures (SQL queries, advanced regression, etc.)
- [ ] Advanced macro functionality
- [ ] Performance optimizations
- [ ] Enhanced data connectivity options

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional statistical procedures
- Macro functionality enhancements
- Performance optimizations
- VS Code extension features
- Documentation and examples

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 [Documentation](https://github.com/ryan-story/Open-SAS/wiki)
- 🐛 [Issue Tracker](https://github.com/ryan-story/Open-SAS/issues)
- 💬 [Discussions](https://github.com/ryan-story/Open-SAS/discussions)