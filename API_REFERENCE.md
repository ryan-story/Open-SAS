# Open-SAS API Reference

## Table of Contents
1. [Core Classes](#core-classes)
2. [Parsers](#parsers)
3. [PROC Implementations](#proc-implementations)
4. [Utilities](#utilities)
5. [Error Handling](#error-handling)
6. [Extension Development](#extension-development)

## Core Classes

### SASInterpreter

The main interpreter class for executing SAS code.

```python
from open_sas import SASInterpreter

interpreter = SASInterpreter()
```

#### Methods

##### `run_file(file_path: str) -> None`
Execute a .osas file.

**Parameters:**
- `file_path` (str): Path to the .osas file

**Example:**
```python
interpreter.run_file('analysis.osas')
```

##### `run_code(sas_code: str) -> None`
Execute SAS code string.

**Parameters:**
- `sas_code` (str): SAS code to execute

**Example:**
```python
interpreter.run_code('data work.test; set work.original; run;')
```

##### `get_data_set(name: str) -> Optional[pd.DataFrame]`
Get a dataset by name.

**Parameters:**
- `name` (str): Dataset name

**Returns:**
- `Optional[pd.DataFrame]`: DataFrame if found, None otherwise

##### `list_data_sets() -> List[str]`
List all available datasets.

**Returns:**
- `List[str]`: List of dataset names

##### `clear_workspace() -> None`
Clear all datasets and reset the workspace.

## Parsers

### DataStepParser

Parser for SAS DATA step syntax.

```python
from open_sas.parser import DataStepParser

parser = DataStepParser()
```

#### Methods

##### `parse_data_step(code: str) -> DataStepInfo`
Parse a complete DATA step.

**Parameters:**
- `code` (str): DATA step code

**Returns:**
- `DataStepInfo`: Parsed DATA step information

##### `parse_datalines(code: str) -> pd.DataFrame`
Parse DATALINES/CARDS section.

**Parameters:**
- `code` (str): DATALINES code

**Returns:**
- `pd.DataFrame`: DataFrame created from data

### ProcParser

Parser for SAS PROC procedure syntax.

```python
from open_sas.parser import ProcParser

parser = ProcParser()
```

#### Methods

##### `parse_proc(code: str) -> ProcStatement`
Parse a PROC procedure.

**Parameters:**
- `code` (str): PROC code

**Returns:**
- `ProcStatement`: Parsed PROC information

### MacroParser

Parser and processor for SAS macro language.

```python
from open_sas.parser import MacroParser

parser = MacroParser()
```

#### Methods

##### `process_macro_code(code: str) -> str`
Process code containing macro constructs.

**Parameters:**
- `code` (str): Code with macro constructs

**Returns:**
- `str`: Code with macros processed

##### `resolve_macro_variables(code: str) -> str`
Resolve macro variable references.

**Parameters:**
- `code` (str): Code with macro variables

**Returns:**
- `str`: Code with variables resolved

## PROC Implementations

### ProcMeans

Implementation of SAS PROC MEANS.

```python
from open_sas.procs import ProcMeans

proc = ProcMeans()
result = proc.execute(data, proc_info)
```

### ProcFreq

Implementation of SAS PROC FREQ.

```python
from open_sas.procs import ProcFreq

proc = ProcFreq()
result = proc.execute(data, proc_info)
```

### ProcPrint

Implementation of SAS PROC PRINT.

```python
from open_sas.procs import ProcPrint

proc = ProcPrint()
result = proc.execute(data, proc_info)
```

### ProcSort

Implementation of SAS PROC SORT.

```python
from open_sas.procs import ProcSort

proc = ProcSort()
result = proc.execute(data, proc_info)
```

### ProcContents

Implementation of SAS PROC CONTENTS.

```python
from open_sas.procs import ProcContents

proc = ProcContents()
result = proc.execute(data, proc_info)
```

### ProcUnivariate

Implementation of SAS PROC UNIVARIATE.

```python
from open_sas.procs import ProcUnivariate

proc = ProcUnivariate()
result = proc.execute(data, proc_info)
```

## Utilities

### ExpressionParser

Parser for SAS expressions and conditions.

```python
from open_sas.utils import ExpressionParser

parser = ExpressionParser()
mask = parser.parse_where_condition("age > 30", data)
```

#### Methods

##### `parse_where_condition(condition: str, data: pd.DataFrame) -> pd.Series`
Parse a WHERE condition.

**Parameters:**
- `condition` (str): WHERE condition
- `data` (pd.DataFrame): DataFrame to apply condition to

**Returns:**
- `pd.Series`: Boolean Series indicating matching rows

### ExpressionEvaluator

Evaluator for SAS expressions in DATA steps.

```python
from open_sas.utils import ExpressionEvaluator

evaluator = ExpressionEvaluator()
data = evaluator.evaluate_assignment("new_var = old_var * 2", data)
```

#### Methods

##### `evaluate_assignment(assignment: str, data: pd.DataFrame) -> pd.DataFrame`
Evaluate a variable assignment.

**Parameters:**
- `assignment` (str): Assignment statement
- `data` (pd.DataFrame): DataFrame to apply assignment to

**Returns:**
- `pd.DataFrame`: DataFrame with new variable

##### `evaluate_if_then_else(if_statement: str, data: pd.DataFrame) -> pd.DataFrame`
Evaluate IF/THEN/ELSE statement.

**Parameters:**
- `if_statement` (str): IF/THEN/ELSE statement
- `data` (pd.DataFrame): DataFrame to apply condition to

**Returns:**
- `pd.DataFrame`: DataFrame with conditional logic applied

### DataUtils

Utility functions for data manipulation.

```python
from open_sas.utils import DataUtils

utils = DataUtils()
filtered_data = utils.apply_where_condition(data, "age > 30", parser)
```

#### Methods

##### `apply_where_condition(df: pd.DataFrame, condition: str, expression_parser) -> pd.DataFrame`
Apply WHERE condition to DataFrame.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to filter
- `condition` (str): WHERE condition
- `expression_parser`: ExpressionParser instance

**Returns:**
- `pd.DataFrame`: Filtered DataFrame

##### `format_dataframe_for_display(df: pd.DataFrame, max_rows: int = 100) -> List[str]`
Format DataFrame for text display.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to format
- `max_rows` (int): Maximum rows to display

**Returns:**
- `List[str]`: Formatted lines

### LibnameManager

Manager for SAS libraries and persistent storage.

```python
from open_sas.utils import LibnameManager

manager = LibnameManager()
manager.create_library('sales', './sales_data')
```

#### Methods

##### `create_library(libname: str, path: str) -> bool`
Create a new library mapping.

**Parameters:**
- `libname` (str): Library name
- `path` (str): Directory path

**Returns:**
- `bool`: True if successful

##### `save_dataset(libname: str, dataset_name: str, data: pd.DataFrame) -> bool`
Save dataset to library.

**Parameters:**
- `libname` (str): Library name
- `dataset_name` (str): Dataset name
- `data` (pd.DataFrame): DataFrame to save

**Returns:**
- `bool`: True if successful

##### `load_dataset(libname: str, dataset_name: str) -> Optional[pd.DataFrame]`
Load dataset from library.

**Parameters:**
- `libname` (str): Library name
- `dataset_name` (str): Dataset name

**Returns:**
- `Optional[pd.DataFrame]`: DataFrame or None if not found

## Error Handling

### ErrorHandler

Comprehensive error handler for SAS code.

```python
from open_sas.utils import ErrorHandler, ErrorType

handler = ErrorHandler()
errors = handler.validate_syntax(code)
```

#### Methods

##### `validate_syntax(code: str) -> List[SASError]`
Validate SAS code syntax.

**Parameters:**
- `code` (str): SAS code to validate

**Returns:**
- `List[SASError]`: List of syntax errors

##### `validate_data_step(data_step_code: str) -> List[SASError]`
Validate DATA step syntax.

**Parameters:**
- `data_step_code` (str): DATA step code

**Returns:**
- `List[SASError]`: List of validation errors

##### `format_errors() -> str`
Format all errors for display.

**Returns:**
- `str`: Formatted error messages

### SASError

Represents a SAS error or warning.

```python
from open_sas.utils import SASError, ErrorType

error = SASError(
    error_type=ErrorType.SYNTAX_ERROR,
    message="Statement not terminated with semicolon",
    line_number=5,
    code_snippet="data work.test"
)
```

#### Attributes

- `error_type` (ErrorType): Type of error
- `message` (str): Error message
- `line_number` (Optional[int]): Line number
- `column` (Optional[int]): Column number
- `code_snippet` (Optional[str]): Code snippet

### ErrorType

Enumeration of error types.

```python
from open_sas.utils import ErrorType

ErrorType.SYNTAX_ERROR
ErrorType.RUNTIME_ERROR
ErrorType.WARNING
ErrorType.NOTE
```

## Extension Development

### Creating Custom PROCs

To create a custom PROC procedure:

```python
from open_sas.parser.proc_parser import ProcStatement
import pandas as pd
from typing import Dict, Any

class CustomProc:
    def __init__(self):
        pass
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        results = {
            'output_text': [],
            'output_data': None
        }
        
        # Your PROC logic here
        results['output_text'].append("Custom PROC executed successfully")
        
        return results
```

### Adding New SAS Functions

To add new SAS functions to the expression evaluator:

```python
from open_sas.utils import ExpressionEvaluator

evaluator = ExpressionEvaluator()

def custom_function(x):
    return x * 2

evaluator.functions['custom_func'] = custom_function
```

### Custom Error Handling

To add custom error handling:

```python
from open_sas.utils import ErrorHandler, ErrorType

handler = ErrorHandler()
handler.add_error(
    ErrorType.WARNING,
    "Custom warning message",
    line_number=10,
    code_snippet="custom code"
)
```

## Data Structures

### DataStepInfo

Information about a parsed DATA step.

```python
@dataclass
class DataStepInfo:
    output_dataset: str
    statements: List[DataStepStatement]
    set_datasets: List[str]
    where_conditions: List[str]
    variable_assignments: List[str]
    drop_vars: List[str]
    keep_vars: List[str]
    rename_vars: Dict[str, str]
    by_vars: List[str]
```

### ProcStatement

Information about a parsed PROC procedure.

```python
@dataclass
class ProcStatement:
    proc_name: str
    options: Dict[str, Any]
    statements: List[str]
    data_option: Optional[str] = None
    output_option: Optional[str] = None
```

### MacroDefinition

Information about a SAS macro definition.

```python
@dataclass
class MacroDefinition:
    name: str
    parameters: List[str]
    body: str
    line_start: int
    line_end: int
```

## Configuration

### Interpreter Configuration

```python
interpreter = SASInterpreter()

# Access components
interpreter.data_step_parser
interpreter.proc_parser
interpreter.macro_parser
interpreter.expression_parser
interpreter.expression_evaluator
interpreter.data_utils
interpreter.libname_manager
interpreter.error_handler
```

### Library Configuration

```python
# Set default work directory
manager = LibnameManager(default_work_dir='/path/to/work')

# Create custom libraries
manager.create_library('sales', '/path/to/sales')
manager.create_library('reports', '/path/to/reports')
```

## Performance Considerations

### Memory Management

- Use WHERE clauses to filter data early
- Clear WORK library periodically
- Use appropriate data types
- Limit observations with OBS= option

### Storage Optimization

- Use Parquet format for large datasets
- Compress data when possible
- Use appropriate column types
- Consider partitioning for very large datasets

### Execution Optimization

- Use vectorized operations when possible
- Avoid loops in DATA steps
- Use appropriate PROC procedures
- Consider parallel processing for large datasets

## Best Practices

### Code Organization

1. Use meaningful dataset names
2. Organize code into logical sections
3. Use comments to document complex logic
4. Follow consistent naming conventions

### Error Handling

1. Validate input data
2. Use appropriate error messages
3. Handle edge cases gracefully
4. Provide helpful debugging information

### Performance

1. Profile code execution
2. Use appropriate data structures
3. Optimize for your specific use case
4. Monitor memory usage

### Testing

1. Test with small datasets first
2. Validate results against known outputs
3. Test edge cases and error conditions
4. Use comprehensive test suites
