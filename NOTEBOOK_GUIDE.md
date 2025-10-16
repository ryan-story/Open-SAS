# Open-SAS Notebook Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Jupyter Notebook Support](#jupyter-notebook-support)
4. [VS Code Notebook Support](#vs-code-notebook-support)
5. [Interactive Analysis](#interactive-analysis)
6. [Rich Output Display](#rich-output-display)
7. [Examples](#examples)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

## Introduction

Open-SAS now supports interactive notebook environments, allowing you to run SAS code cell by cell with rich output display. This makes data analysis more interactive and exploratory, similar to Jupyter notebooks but with authentic SAS syntax.

### Key Features

- **🔬 Interactive Execution**: Run SAS code cell by cell
- **📊 Rich Output**: Visualize datasets and PROC results
- **🔄 Iterative Development**: Test code snippets interactively
- **📝 Mixed Content**: Combine code, output, and markdown
- **🎯 Data Exploration**: Quick analysis and visualization
- **📚 Learning**: Interactive SAS tutorials and examples

## Installation

### Install with Notebook Support

```bash
# Install Open-SAS with notebook dependencies
pip install open-sas[notebook]

# Install the Jupyter kernel
python -m open_sas.kernel install
```

### Verify Installation

```bash
# Check if kernel is installed
jupyter kernelspec list

# You should see 'osas' in the list
```

## Jupyter Notebook Support

### Creating a Jupyter Notebook

1. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Create New Notebook**:
   - Click "New" → "Open-SAS"
   - Or create a new notebook and change kernel to "Open-SAS"

3. **Write SAS Code**:
   ```sas
   data work.sample;
       input name $ age salary;
       datalines;
   John 30 60000
   Mary 25 55000
   Bob 35 75000
   ;
   run;
   ```

4. **Run Cells**:
   - Press `Shift + Enter` to run a cell
   - See rich output with dataset displays

### Jupyter Lab Support

```bash
# Install JupyterLab
pip install jupyterlab

# Start JupyterLab
jupyter lab

# Create Open-SAS notebook
# File → New → Notebook → Select "Open-SAS" kernel
```

## VS Code Notebook Support

### Using .osasnb Files

1. **Create Notebook File**:
   - Create a file with `.osasnb` extension
   - VS Code will recognize it as an Open-SAS notebook

2. **Add Cells**:
   - Use `Ctrl+Shift+P` → "Notebook: Insert Code Cell"
   - Set language to "osas"

3. **Run Cells**:
   - Click the "Run" button above each cell
   - Or use `Ctrl+Shift+Enter`

### Sample .osasnb File

```json
{
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "data work.test;\n",
        "    input id name $ age;\n",
        "    datalines;\n",
        "1 Alice 30\n",
        "2 Bob 35\n",
        ";\n",
        "run;"
      ],
      "language": "osas"
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Open-SAS",
      "language": "osas",
      "name": "osas"
    }
  }
}
```

## Interactive Analysis

### Basic Workflow

1. **Create Data**:
   ```sas
   data work.sales;
       input customer_id name $ sales_amount;
       datalines;
   1 John 50000
   2 Mary 75000
   3 Bob 60000
   ;
   run;
   ```

2. **Explore Data**:
   ```sas
   proc print data=work.sales;
   run;
   ```

3. **Analyze Data**:
   ```sas
   proc means data=work.sales;
       var sales_amount;
   run;
   ```

4. **Filter Data**:
   ```sas
   data work.high_sales;
       set work.sales;
       where sales_amount > 60000;
   run;
   ```

### Advanced Features

#### Macro Variables
```sas
%let threshold = 60000;

data work.filtered;
    set work.sales;
    where sales_amount >= &threshold;
run;
```

#### Cross-Library Operations
```sas
libname analysis './analysis_data';

data analysis.results;
    set work.sales;
    if sales_amount > 70000 then category = 'High';
    else category = 'Standard';
run;
```

## Rich Output Display

### Dataset Display

When you create or modify datasets, Open-SAS automatically displays:
- **Dataset Information**: Shape, columns, data types
- **Data Preview**: First few rows in formatted table
- **Memory Usage**: Storage information
- **Null Counts**: Missing data summary

### PROC Results

PROC procedures display rich output:
- **PROC MEANS**: Formatted statistics tables
- **PROC FREQ**: Frequency tables with percentages
- **PROC PRINT**: Formatted data display
- **PROC CONTENTS**: Dataset metadata

### Error Display

Errors are displayed with:
- **Syntax Errors**: Highlighted with line numbers
- **Runtime Errors**: Clear error messages
- **Warnings**: Non-fatal issues
- **Notes**: Informational messages

## Examples

### Sales Analysis Notebook

```sas
/* Cell 1: Create sales data */
data work.sales_data;
    input customer_id name $ age region $ sales_amount;
    datalines;
1 John 35 North 50000
2 Mary 28 South 75000
3 Bob 42 East 60000
4 Alice 31 West 80000
5 Charlie 29 North 55000
;
run;

/* Cell 2: Display data */
proc print data=work.sales_data;
run;

/* Cell 3: Descriptive statistics */
proc means data=work.sales_data;
    var age sales_amount;
run;

/* Cell 4: Frequency analysis */
proc freq data=work.sales_data;
    tables region;
run;

/* Cell 5: Create high performers */
%let min_sales = 70000;

data work.high_performers;
    set work.sales_data;
    where sales_amount >= &min_sales;
run;

/* Cell 6: Display results */
proc print data=work.high_performers;
run;
```

### Employee Analysis Notebook

```sas
/* Cell 1: Employee data */
data work.employees;
    input emp_id name $ age salary department $;
    datalines;
1 John 35 50000 Sales
2 Mary 28 60000 IT
3 Bob 42 75000 Sales
4 Alice 31 55000 HR
;
run;

/* Cell 2: Department analysis */
proc means data=work.employees;
    var salary;
    by department;
run;

/* Cell 3: Age groups */
data work.age_analysis;
    set work.employees;
    if age >= 40 then age_group = 'Senior';
    else if age >= 30 then age_group = 'Mid';
    else age_group = 'Junior';
run;

/* Cell 4: Age group frequencies */
proc freq data=work.age_analysis;
    tables age_group;
run;
```

## Advanced Features

### Workspace Management

```python
# In a Python cell (if using mixed kernel)
from open_sas.notebook_interpreter import NotebookSASInterpreter

interpreter = NotebookSASInterpreter()

# Get workspace summary
workspace = interpreter.get_workspace_summary()
print(f"Datasets: {workspace['datasets']}")
print(f"Libraries: {workspace['libraries']}")
```

### Export Functionality

```python
# Export dataset to different formats
json_data = interpreter.export_dataset('work.sales', 'json')
csv_data = interpreter.export_dataset('work.sales', 'csv')
html_data = interpreter.export_dataset('work.sales', 'html')
```

### Execution History

```python
# Get execution history
history = interpreter.get_execution_history()
for i, execution in enumerate(history):
    print(f"Execution {i+1}: {execution['success']}")
```

## Troubleshooting

### Common Issues

#### Kernel Not Found
```
ERROR: No kernel named 'osas' found
```
**Solution**: Install the kernel
```bash
python -m open_sas.kernel install
```

#### Import Errors
```
ERROR: Open-SAS package not found
```
**Solution**: Install Open-SAS
```bash
pip install open-sas[notebook]
```

#### VS Code Notebook Not Working
```
ERROR: Notebook provider not found
```
**Solution**: 
1. Install the Open-SAS VS Code extension
2. Reload VS Code
3. Create `.osasnb` file

### Debugging Tips

1. **Check Kernel Installation**:
   ```bash
   jupyter kernelspec list
   ```

2. **Test Kernel Manually**:
   ```bash
   python -m open_sas.kernel
   ```

3. **Check VS Code Extension**:
   - Open Command Palette (`Ctrl+Shift+P`)
   - Search for "Open-SAS"

4. **View Output**:
   - Check VS Code Output panel
   - Look for "Open-SAS Output" channel

### Performance Tips

1. **Use WHERE Clauses**: Filter data early in analysis
2. **Limit Observations**: Use OBS= option for large datasets
3. **Clear Workspace**: Periodically clear datasets
4. **Use Libraries**: Organize data in libraries

## Best Practices

### Notebook Organization

1. **Structure**: Use markdown cells for documentation
2. **Comments**: Add comments to explain complex logic
3. **Chunking**: Break complex analysis into logical chunks
4. **Naming**: Use descriptive dataset and variable names

### Data Analysis Workflow

1. **Load Data**: Create or import datasets
2. **Explore**: Use PROC PRINT and PROC CONTENTS
3. **Clean**: Handle missing values and outliers
4. **Analyze**: Run statistical procedures
5. **Visualize**: Create summaries and reports
6. **Export**: Save results for further use

### Collaboration

1. **Version Control**: Use Git for notebook files
2. **Documentation**: Include markdown explanations
3. **Reproducibility**: Use consistent data sources
4. **Sharing**: Export results in standard formats

## Conclusion

Open-SAS notebook support provides a powerful, interactive environment for SAS data analysis. Whether you're using Jupyter notebooks or VS Code, you can now enjoy the benefits of:

- **Interactive Development**: Test code snippets quickly
- **Rich Visualization**: See data and results immediately
- **Iterative Analysis**: Build analysis step by step
- **Documentation**: Mix code, output, and explanations
- **Learning**: Explore SAS syntax interactively

The notebook environment makes Open-SAS even more accessible and powerful for data analysis workflows!
