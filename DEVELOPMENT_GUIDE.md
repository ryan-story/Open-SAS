# Open-SAS Development Guide

## Quick Start for Development

### 1. **Open the Project in VS Code**

```bash
cd "/Users/rs255/My Technologies/Open-SAS"
code .
```

### 2. **Install Dependencies**

```bash
# Install Python dependencies
pip install -e .

# Install VS Code extension dependencies
cd vscode-extension
npm install
```

### 3. **Test the Extension**

The Open-SAS extension is now installed in your VS Code! You can:

- **Open any .osas file** - You'll get syntax highlighting
- **Use Command Palette** (`Ctrl+Shift+P`):
  - "Open-SAS: Run File" - Execute the current .osas file
  - "Open-SAS: Run Selection" - Execute selected code
  - "Open-SAS: Check Syntax" - Validate syntax

### 4. **Development Workflow**

#### **A. Test Python Backend**
```bash
# Run basic tests
python test_basic.py

# Run comprehensive tests
python test_comprehensive.py

# Test notebook functionality
python test_notebook.py
```

#### **B. Test VS Code Extension**
1. **Open a .osas file** (like `examples/basic_analysis.osas`)
2. **Use Command Palette** to run the file
3. **Check Output Panel** for results

#### **C. Modify and Test**
1. **Edit Python code** in `open_sas/` directory
2. **Test changes** with Python scripts
3. **Reload VS Code** to pick up changes

### 5. **Available Development Tools**

#### **VS Code Tasks** (`Ctrl+Shift+P` → "Tasks: Run Task")
- **"Run Open-SAS File"** - Execute current .osas file
- **"Test Open-SAS"** - Run basic tests
- **"Build VS Code Extension"** - Compile extension

#### **VS Code Debugging** (`F5` or `Ctrl+Shift+P` → "Debug: Start Debugging")
- **"Run Open-SAS Test"** - Debug test scripts
- **"Run Open-SAS CLI"** - Debug CLI interface
- **"Test Notebook Functionality"** - Debug notebook features

### 6. **File Structure for Development**

```
Open-SAS/
├── open_sas/                 # Python package
│   ├── __init__.py          # Main exports
│   ├── interpreter.py       # Core SAS interpreter
│   ├── cli.py              # Command-line interface
│   ├── parser/             # SAS syntax parsers
│   ├── procs/              # PROC implementations
│   ├── utils/              # Utility functions
│   └── kernel/             # Jupyter kernel
├── vscode-extension/        # VS Code extension
│   ├── src/                # TypeScript source
│   ├── out/                # Compiled JavaScript
│   └── package.json        # Extension manifest
├── examples/               # Example .osas files
├── test_*.py              # Test scripts
└── .vscode/               # VS Code configuration
```

### 7. **Testing Your Changes**

#### **Python Backend Testing**
```bash
# Test specific functionality
python -c "
from open_sas import SASInterpreter
interpreter = SASInterpreter()
interpreter.run_code('data work.test; input x; datalines; 1; run; proc print; run;')
"

# Test with your own .osas file
python -c "from open_sas import SASInterpreter; interpreter = SASInterpreter(); interpreter.run_file('your_file.osas')"
```

#### **VS Code Extension Testing**
1. **Make changes** to TypeScript files in `vscode-extension/src/`
2. **Compile** with `npm run compile` in `vscode-extension/`
3. **Reload VS Code** (`Ctrl+Shift+P` → "Developer: Reload Window")
4. **Test** by opening .osas files and using commands

### 8. **Creating New Features**

#### **Add New PROC Procedure**
1. **Create** `open_sas/procs/proc_newproc.py`
2. **Implement** the `execute()` method
3. **Register** in `open_sas/interpreter.py`
4. **Test** with sample code

#### **Add New SAS Functions**
1. **Edit** `open_sas/utils/expression_evaluator.py`
2. **Add** function to `self.functions` dictionary
3. **Test** with DATA step assignments

#### **Enhance VS Code Extension**
1. **Edit** TypeScript files in `vscode-extension/src/`
2. **Add** new commands in `package.json`
3. **Compile** and test

### 9. **Debugging Tips**

#### **Python Debugging**
```python
# Add debug prints
print(f"Debug: {variable}")

# Use Python debugger
import pdb; pdb.set_trace()

# Check interpreter state
print(f"Datasets: {interpreter.list_data_sets()}")
print(f"Libraries: {interpreter.libname_manager.list_libraries()}")
```

#### **VS Code Extension Debugging**
1. **Open Developer Tools** (`Help` → `Toggle Developer Tools`)
2. **Check Console** for errors
3. **Use Output Panel** to see extension logs
4. **Reload Window** after changes

### 10. **Publishing the Extension**

#### **Package Extension**
```bash
cd vscode-extension
vsce package
```

#### **Install Locally**
```bash
code --install-extension open-sas-0.1.0.vsix
```

#### **Publish to Marketplace**
```bash
vsce publish
```

## 🎯 **Ready to Develop!**

You now have a complete development environment set up. You can:

- ✅ **Write SAS code** in .osas files with syntax highlighting
- ✅ **Run code** directly from VS Code
- ✅ **Debug** Python backend and VS Code extension
- ✅ **Test** all functionality
- ✅ **Modify** and extend the system
- ✅ **Package** and distribute the extension

**Start coding in Open-SAS right now!** 🚀
