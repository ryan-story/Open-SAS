# Open-SAS

A Python-based SAS interpreter with VS Code extension support. Write SAS code in `.osas` files with full syntax highlighting and Python backend execution.

## Overview

Open-SAS bridges the gap between SAS and Python by providing:
- **SAS-like syntax** for data manipulation and analysis
- **Python backend** for execution and performance
- **VS Code extension** with syntax highlighting and IntelliSense
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Open source** and free to use

## Features

### Core Interpreter
- SAS DATA step functionality
- Major PROC procedures (PROC SQL, PROC MEANS, PROC FREQ, etc.)
- SAS-style data manipulation and analysis
- Python pandas/numpy backend for performance

### VS Code Extension
- Syntax highlighting for `.osas` files
- IntelliSense and code completion
- Error detection and reporting
- Integrated terminal for execution
- Code snippets for common SAS patterns
- **Notebook support** for interactive analysis

### Supported SAS Features
- **DATA Steps**: Variable creation, conditional logic, loops
- **PROC SQL**: SQL queries with SAS-specific functions
- **PROC MEANS**: Descriptive statistics
- **PROC FREQ**: Frequency tables and crosstabs
- **PROC SORT**: Data sorting and deduplication
- **PROC PRINT**: Data display and formatting
- **Macro variables**: %LET, %PUT, %IF statements
- **Libraries**: LIBNAME functionality

## Installation

### Python Package
```bash
pip install open-sas
```

### VS Code Extension
1. Install from VS Code Marketplace: "Open-SAS"
2. Or install from source (see Development section)

## Quick Start

### 1. Create a .osas file
```sas
/* example.osas */
data work.sample;
    set sashelp.class;
    where age > 12;
    bmi = weight / (height**2);
run;

proc means data=work.sample;
    var age height weight bmi;
run;
```

### 2. Run with Python
```python
from open_sas import SASInterpreter

interpreter = SASInterpreter()
interpreter.run_file('example.osas')
```

### 3. Or use VS Code
- Open `.osas` file in VS Code
- Use `Ctrl+Shift+P` → "Open-SAS: Run File"
- View results in integrated terminal

### 4. Or use Interactive Notebooks
- Install with notebook support: `pip install open-sas[notebook]`
- Install kernel: `python -m open_sas.kernel install`
- Create Jupyter notebook with Open-SAS kernel
- Or create `.osasnb` file in VS Code

## Project Structure

```
Open-SAS/
├── open_sas/                 # Core Python package
│   ├── __init__.py
│   ├── interpreter.py        # Main SAS interpreter
│   ├── parser/              # SAS syntax parser
│   ├── procs/               # PROC procedure implementations
│   └── utils/               # Utility functions
├── vscode-extension/         # VS Code extension
│   ├── package.json
│   ├── syntaxes/            # SAS syntax definitions
│   └── src/                 # Extension source code
├── examples/                # Example .osas files
├── tests/                   # Test suite
├── docs/                    # Documentation
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
pytest tests/
```

### Building VS Code Extension
```bash
cd vscode-extension
npm install
npm run compile
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Additional PROC procedures
- SAS macro functionality
- Performance optimizations
- VS Code extension features
- Documentation and examples

## Roadmap

- [ ] Core DATA step implementation
- [ ] Essential PROC procedures (SQL, MEANS, FREQ, SORT)
- [ ] VS Code extension with syntax highlighting
- [ ] Macro variable support
- [ ] Library (LIBNAME) functionality
- [ ] Advanced PROC procedures (REG, GLM, etc.)
- [ ] SAS/ACCESS compatibility layer
- [ ] Performance benchmarking vs native SAS

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by the need for open-source SAS alternatives
- Built on top of Python's excellent data science ecosystem
- Thanks to the SAS community for syntax inspiration

## Support

- 📖 [Documentation](https://github.com/ryan-story/Open-SAS/wiki)
- 🐛 [Issue Tracker](https://github.com/ryan-story/Open-SAS/issues)
- 💬 [Discussions](https://github.com/ryan-story/Open-SAS/discussions)