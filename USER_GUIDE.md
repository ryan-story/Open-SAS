# Open-SAS User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [DATA Steps](#data-steps)
5. [PROC Procedures](#proc-procedures)
6. [Macro Language](#macro-language)
7. [LIBNAME and Libraries](#libname-and-libraries)
8. [VS Code Extension](#vs-code-extension)
9. [Command Line Interface](#command-line-interface)
10. [Examples](#examples)
11. [Troubleshooting](#troubleshooting)

## Introduction

Open-SAS is a Python-based SAS interpreter that provides a complete open-source alternative to SAS. It supports authentic SAS syntax while leveraging Python's powerful data science ecosystem for execution.

### Key Features

- **Authentic SAS Syntax**: Write SAS code using familiar DATA steps and PROC procedures
- **Python Backend**: High-performance data processing using pandas and numpy
- **Persistent Storage**: Parquet-based storage for efficient data management
- **VS Code Integration**: Full syntax highlighting and execution support
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Open Source**: Free and extensible

## Installation

### Python Package

```bash
pip install open-sas
```

### VS Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Open-SAS"
4. Click Install

### Development Installation

```bash
git clone https://github.com/ryan-story/Open-SAS.git
cd Open-SAS
pip install -e .
```

## Quick Start

### 1. Create a .osas file

```sas
/* example.osas */
data work.sample;
    input name $ age height weight;
    datalines;
John 25 70 180
Mary 30 65 140
Bob 35 72 200
Alice 28 68 160
;
run;

proc means data=work.sample;
    var age height weight;
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

## DATA Steps

DATA steps are the core of SAS programming. Open-SAS supports comprehensive DATA step functionality.

### Basic DATA Step

```sas
data work.new_dataset;
    set work.existing_dataset;
    new_variable = old_variable * 2;
run;
```

### Creating Data with DATALINES

```sas
data work.survey_data;
    input respondent_id age gender $ income;
    datalines;
1 25 M 50000
2 30 F 60000
3 35 M 75000
4 28 F 55000
;
run;
```

### WHERE Clauses

```sas
data work.filtered_data;
    set work.original_data;
    where age > 30 and income > 60000;
run;
```

### IF/THEN/ELSE Statements

```sas
data work.categorized_data;
    set work.original_data;
    if income >= 70000 then category = 'High';
    else if income >= 50000 then category = 'Medium';
    else category = 'Low';
run;
```

### Variable Manipulation

```sas
data work.enhanced_data;
    set work.original_data;
    annual_bonus = salary * 0.1;
    total_compensation = salary + annual_bonus;
    salary_per_year = salary / age;
run;
```

### DROP, KEEP, and RENAME

```sas
data work.final_data;
    set work.original_data;
    drop unwanted_variable;
    keep id name salary;
    rename old_name = new_name;
run;
```

## PROC Procedures

Open-SAS implements essential SAS procedures for data analysis.

### PROC PRINT

Display dataset contents:

```sas
proc print data=work.sample;
run;
```

With WHERE clause:

```sas
proc print data=work.sample;
    where age > 30;
run;
```

### PROC MEANS

Descriptive statistics:

```sas
proc means data=work.sample;
    var age height weight;
run;
```

Grouped analysis:

```sas
proc means data=work.sample;
    var salary;
    by department;
run;
```

### PROC FREQ

Frequency tables:

```sas
proc freq data=work.sample;
    tables gender department;
run;
```

Cross-tabulation:

```sas
proc freq data=work.sample;
    tables gender * department;
run;
```

### PROC SORT

Sort data:

```sas
proc sort data=work.sample;
    by descending salary;
run;
```

Remove duplicates:

```sas
proc sort data=work.sample nodupkey;
    by id;
run;
```

### PROC CONTENTS

Dataset information:

```sas
proc contents data=work.sample;
run;
```

### PROC UNIVARIATE

Detailed univariate analysis:

```sas
proc univariate data=work.sample;
    var salary;
run;
```

## Macro Language

Open-SAS supports SAS macro functionality for dynamic code generation.

### Macro Variables

```sas
%let cutoff = 50000;
%let department = Sales;

proc print data=work.employees;
    where salary > &cutoff and dept = "&department";
run;
```

### Macro Definitions

```sas
%macro analyze_data(dataset, variable);
    proc means data=&dataset;
        var &variable;
    run;
%mend analyze_data;

%analyze_data(work.sample, salary);
```

### Conditional Macros

```sas
%macro conditional_analysis(dataset, type);
    %if &type = summary %then %do;
        proc means data=&dataset;
        run;
    %end;
    %else %do;
        proc freq data=&dataset;
        run;
    %end;
%mend conditional_analysis;
```

## LIBNAME and Libraries

Open-SAS supports SAS library management with persistent storage.

### Creating Libraries

```sas
libname sales './sales_data';
libname reports './reports';
```

### Using Libraries

```sas
data sales.customers;
    input customer_id name $ age;
    datalines;
1 John 35
2 Mary 28
;
run;

proc print data=sales.customers;
run;
```

### Cross-Library Operations

```sas
data reports.summary;
    set sales.customers;
    if age > 30 then category = 'Senior';
    else category = 'Junior';
run;
```

### WORK Library

The WORK library is automatically available for temporary datasets:

```sas
data work.temp_data;
    set sales.customers;
    where age > 25;
run;
```

## VS Code Extension

The Open-SAS VS Code extension provides a complete development environment.

### Features

- **Syntax Highlighting**: Full SAS syntax support
- **Code Snippets**: Common SAS patterns
- **Run Commands**: Execute files and selections
- **Output Streaming**: Real-time results
- **Error Detection**: Syntax validation

### Commands

- `Open-SAS: Run File` - Execute the current .osas file
- `Open-SAS: Run Selection` - Execute selected code
- `Open-SAS: Check Syntax` - Validate syntax

### Configuration

Add to VS Code settings:

```json
{
    "open-sas.pythonPath": "/usr/bin/python3",
    "open-sas.openSASPath": "/path/to/osas_runner.py",
    "open-sas.showOutputOnRun": true
}
```

## Command Line Interface

Open-SAS provides a command-line interface for batch processing.

### Basic Usage

```bash
open-sas program.osas
```

### Interactive Mode

```bash
open-sas -i
```

### Options

```bash
open-sas --help
open-sas --version
open-sas -v program.osas  # Verbose output
```

### Interactive Commands

- `help` - Show help
- `clear` - Clear workspace
- `list` - List datasets
- `quit` - Exit

## Examples

### Sales Analysis

```sas
/* sales_analysis.osas */
libname sales './sales_data';

data sales.transactions;
    input transaction_id customer_id amount date;
    datalines;
1 101 150.00 20240101
2 102 275.50 20240102
3 101 89.99 20240103
4 103 450.00 20240104
5 102 125.00 20240105
;
run;

proc means data=sales.transactions;
    var amount;
run;

proc freq data=sales.transactions;
    tables customer_id;
run;

data sales.customer_summary;
    set sales.transactions;
    by customer_id;
    if first.customer_id then total_amount = 0;
    total_amount + amount;
    if last.customer_id then output;
run;
```

### Employee Analysis

```sas
/* employee_analysis.osas */
data work.employees;
    input emp_id name $ age salary department $;
    datalines;
1 John 35 50000 Sales
2 Mary 28 60000 IT
3 Bob 42 75000 Sales
4 Alice 31 55000 HR
;
run;

%let min_salary = 60000;

data work.high_earners;
    set work.employees;
    where salary >= &min_salary;
    if department = 'Sales' then bonus = salary * 0.15;
    else bonus = salary * 0.10;
    total_compensation = salary + bonus;
run;

proc print data=work.high_earners;
run;

proc means data=work.employees;
    var salary;
    by department;
run;
```

## Troubleshooting

### Common Issues

#### Python Not Found
```
ERROR: Python not found
```
**Solution**: Install Python 3.8+ or set the `open-sas.pythonPath` setting.

#### Dataset Not Found
```
ERROR: Dataset work.sample not found
```
**Solution**: Ensure the dataset exists and is properly created before use.

#### Syntax Errors
```
ERROR: Statement not terminated with semicolon
```
**Solution**: Add semicolons to all statements.

#### Library Errors
```
ERROR: Library sales not found
```
**Solution**: Create the library with `libname sales 'path';` before use.

### Debugging Tips

1. **Use PROC PRINT** to inspect datasets
2. **Check macro variables** with %PUT statements
3. **Validate syntax** with the VS Code extension
4. **Use WHERE clauses** to filter data for testing
5. **Check library paths** and file permissions

### Performance Tips

1. **Use WHERE clauses** to filter data early
2. **Limit observations** with OBS= option in PROCs
3. **Use appropriate data types** for variables
4. **Clear WORK library** periodically
5. **Use Parquet format** for large datasets

### Getting Help

- **Documentation**: Check this user guide
- **Examples**: See the examples/ directory
- **Issues**: Report bugs on GitHub
- **Community**: Join discussions on GitHub

## Conclusion

Open-SAS provides a powerful, open-source alternative to SAS with authentic syntax and modern Python backend. Whether you're analyzing data, creating reports, or building data pipelines, Open-SAS gives you the tools you need to be productive.

For more information, visit the [Open-SAS GitHub repository](https://github.com/ryan-story/Open-SAS).
