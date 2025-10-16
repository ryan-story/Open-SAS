"""
Main SAS interpreter class for Open-SAS.

This module contains the core SASInterpreter class that parses and executes
SAS code using Python as the backend.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import re
import os
from .parser.data_step_parser import DataStepParser
from .parser.proc_parser import ProcParser
from .parser.macro_parser import MacroParser
from .procs import (
    ProcMeans, ProcFreq, ProcPrint, ProcSort, 
    ProcContents, ProcUnivariate
)
from .utils.expression_parser import ExpressionParser
from .utils.expression_evaluator import ExpressionEvaluator
from .utils.data_utils import DataUtils
from .utils.libname_manager import LibnameManager
from .utils.error_handler import ErrorHandler, ErrorType


class SASInterpreter:
    """
    Main interpreter for SAS code execution.
    
    This class provides the core functionality to parse and execute
    SAS-like code using Python libraries as the backend.
    """
    
    def __init__(self):
        """Initialize the SAS interpreter."""
        self.data_sets: Dict[str, pd.DataFrame] = {}
        self.libraries: Dict[str, str] = {}
        self.macro_variables: Dict[str, str] = {}
        self.options: Dict[str, Any] = {}
        
        # Initialize parsers
        self.data_step_parser = DataStepParser()
        self.proc_parser = ProcParser()
        self.macro_parser = MacroParser()
        self.expression_parser = ExpressionParser()
        self.expression_evaluator = ExpressionEvaluator()
        self.data_utils = DataUtils()
        self.libname_manager = LibnameManager()
        self.error_handler = ErrorHandler()
        
        # Initialize PROC implementations
        self.proc_implementations = {
            'MEANS': ProcMeans(),
            'FREQ': ProcFreq(),
            'PRINT': ProcPrint(),
            'SORT': ProcSort(),
            'CONTENTS': ProcContents(),
            'UNIVARIATE': ProcUnivariate()
        }
        
    def run_file(self, file_path: str) -> None:
        """
        Execute a .osas file.
        
        Args:
            file_path: Path to the .osas file to execute
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, 'r') as f:
            sas_code = f.read()
            
        self.run_code(sas_code)
    
    def run_code(self, sas_code: str) -> None:
        """
        Execute SAS code string.
        
        Args:
            sas_code: SAS code to execute
        """
        # First, process macro language constructs
        processed_code = self.macro_parser.process_macro_code(sas_code)
        
        # Remove comments and clean up code
        cleaned_code = self._clean_code(processed_code)
        
        # Split into statements
        statements = self._split_statements(cleaned_code)
        
        # Execute each statement
        for statement in statements:
            if statement.strip():
                self._execute_statement(statement.strip())
    
    def _clean_code(self, code: str) -> str:
        """Remove comments and clean up SAS code."""
        # Remove /* */ comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # Remove * comments (single line)
        lines = code.split('\n')
        cleaned_lines = []
        for line in lines:
            # Find * comments that are not part of strings
            comment_pos = line.find('*')
            if comment_pos != -1:
                # Check if it's not in a string
                before_comment = line[:comment_pos]
                if before_comment.count("'") % 2 == 0 and before_comment.count('"') % 2 == 0:
                    line = line[:comment_pos]
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _split_statements(self, code: str) -> List[str]:
        """Split SAS code into individual statements."""
        print(f"Splitting code: {repr(code)}")
        lines = code.split('\n')
        print(f"Code lines: {lines}")
        statements = []
        current_statement = ""
        in_datalines = False
        in_data_step = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_statement:
                    current_statement += '\n'
                continue
                
            # Check for DATA step start
            if line.upper().startswith('DATA '):
                in_data_step = True
                current_statement = line
                continue
            elif line.upper().startswith('PROC '):
                # End current statement if in DATA step
                if in_data_step and current_statement.strip():
                    statements.append(current_statement.strip())
                    current_statement = ""
                    in_data_step = False
                    in_datalines = False
                # Don't end PROC statement at semicolon, wait for RUN
                if line.endswith(';'):
                    current_statement = line[:-1]  # Remove semicolon
                else:
                    current_statement = line
                continue
            elif line.upper() == 'RUN;':
                if current_statement.strip():
                    current_statement += '\n' + line
                    statements.append(current_statement.strip())
                    current_statement = ""
                    in_data_step = False
                    in_datalines = False
                continue
                
            # Check for DATALINES/CARDS
            if line.upper() in ['DATALINES;', 'CARDS;']:
                in_datalines = True
                current_statement += '\n' + line
                continue
            elif line == ';' and in_datalines:
                current_statement += '\n' + line
                in_datalines = False
                continue
            elif in_datalines:
                current_statement += '\n' + line
                continue
            
            # Regular statement processing
            if in_data_step:
                current_statement += '\n' + line
            elif line.endswith(';'):
                current_statement += ' ' + line
                statements.append(current_statement.strip())
                current_statement = ""
            else:
                # Check if this is a new statement (starts with a keyword)
                if line.upper().startswith(('TABLES', 'VAR', 'BY', 'CLASS', 'MODEL', 'OUTPUT', 'WHERE')):
                    if current_statement.strip():
                        statements.append(current_statement.strip())
                    current_statement = line
                else:
                    current_statement += ' ' + line
        
        # Add the last statement if it doesn't end with semicolon
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        return statements
    
    def _execute_statement(self, statement: str) -> None:
        """Execute a single SAS statement."""
        statement = statement.strip()
        if not statement:
            return
        
        # Determine statement type and execute
        if statement.upper().startswith('DATA '):
            self._execute_data_step(statement)
        elif statement.upper().startswith('PROC '):
            self._execute_proc(statement)
        elif statement.upper().startswith('LIBNAME '):
            self._execute_libname(statement)
        elif statement.upper().startswith('%LET '):
            self._execute_let(statement)
        elif statement.upper() == 'RUN;':
            # RUN statement - currently no-op, but could be used for validation
            pass
        else:
            print(f"Warning: Unsupported statement: {statement}")
    
    def _execute_data_step(self, statement: str) -> None:
        """Execute a DATA step."""
        print(f"Executing DATA step: {statement}")
        
        try:
            # Check if this is a complete DATA step with DATALINES
            if 'datalines' in statement.lower() or 'cards' in statement.lower():
                # Parse DATALINES directly
                input_data = self.data_step_parser.parse_datalines(statement)
                if input_data is not None and not input_data.empty:
                    # Extract output dataset name
                    lines = statement.split('\n')
                    for line in lines:
                        if line.strip().upper().startswith('DATA '):
                            match = re.match(r'data\s+([^;]+)', line, re.IGNORECASE)
                            if match:
                                output_dataset = match.group(1).strip()
                                self.data_sets[output_dataset] = input_data
                                
                                # Save to library if it's a library.dataset format
                                if '.' in output_dataset:
                                    libname, dataset_name = output_dataset.split('.', 1)
                                    if self.libname_manager.save_dataset(libname, dataset_name, input_data):
                                        print(f"Saved dataset {output_dataset} to library {libname}")
                                
                                # Dataset creation message will be printed in the main execution path
                                return
            else:
                # Parse the DATA step normally
                data_info = self.data_step_parser.parse_data_step(statement)
                
                # Get input data
                input_data = None
                if data_info.set_datasets:
                    # For now, just use the first dataset
                    dataset_name = data_info.set_datasets[0]
                    
                    # Check if it's in memory first
                    if dataset_name in self.data_sets:
                        input_data = self.data_sets[dataset_name].copy()
                    else:
                        # Try to load from library
                        if '.' in dataset_name:
                            libname, lib_dataset_name = dataset_name.split('.', 1)
                            loaded_data = self.libname_manager.load_dataset(libname, lib_dataset_name)
                            if loaded_data is not None:
                                input_data = loaded_data.copy()
                                # Also store in memory for future use
                                self.data_sets[dataset_name] = input_data
                            else:
                                print(f"ERROR: Dataset {dataset_name} not found in library {libname}")
                                return
                        else:
                            print(f"ERROR: Dataset {dataset_name} not found")
                            return
                else:
                    # Create empty dataset
                    input_data = pd.DataFrame()
                
                if input_data is not None:
                    # Apply WHERE conditions
                    for where_condition in data_info.where_conditions:
                        print(f"Applying WHERE condition: {where_condition}")
                        input_data = self.data_utils.apply_where_condition(
                            input_data, where_condition, self.expression_parser
                        )
                    
                    # Apply variable assignments
                    for assignment in data_info.variable_assignments:
                        print(f"Processing assignment: {assignment}")
                        if assignment.lower().startswith('if '):
                            # Handle IF/THEN/ELSE statements
                            input_data = self.expression_evaluator.evaluate_if_then_else(assignment, input_data)
                        else:
                            # Handle regular assignments
                            input_data = self.expression_evaluator.evaluate_assignment(assignment, input_data)
                    
                    # Apply DROP/KEEP
                    if data_info.drop_vars:
                        input_data = self.data_utils.drop_columns(input_data, data_info.drop_vars)
                    
                    if data_info.keep_vars:
                        input_data = self.data_utils.select_columns(input_data, data_info.keep_vars)
                    
                    # Apply RENAME
                    if data_info.rename_vars:
                        input_data = self.data_utils.rename_columns(input_data, data_info.rename_vars)
                    
                    # Store the result
                    self.data_sets[data_info.output_dataset] = input_data
                    
                    # Save to library if it's a library.dataset format
                    if '.' in data_info.output_dataset:
                        libname, dataset_name = data_info.output_dataset.split('.', 1)
                        if self.libname_manager.save_dataset(libname, dataset_name, input_data):
                            print(f"Saved dataset {data_info.output_dataset} to library {libname}")
                    
                    print(f"Created dataset: {data_info.output_dataset} with {len(input_data)} observations")
            
        except Exception as e:
            print(f"ERROR in DATA step: {e}")
            import traceback
            traceback.print_exc()
    
    def _execute_proc(self, statement: str) -> None:
        """Execute a PROC procedure."""
        print(f"Executing PROC: {statement}")
        
        try:
            # Parse the PROC statement
            proc_info = self.proc_parser.parse_proc(statement)
            
            # Get input data
            input_data = None
            if proc_info.data_option:
                dataset_name = proc_info.data_option
                
                # Check if it's in memory first
                if dataset_name in self.data_sets:
                    input_data = self.data_sets[dataset_name]
                else:
                    # Try to load from library
                    if '.' in dataset_name:
                        libname, lib_dataset_name = dataset_name.split('.', 1)
                        loaded_data = self.libname_manager.load_dataset(libname, lib_dataset_name)
                        if loaded_data is not None:
                            input_data = loaded_data
                            # Also store in memory for future use
                            self.data_sets[dataset_name] = input_data
                        else:
                            print(f"ERROR: Dataset {dataset_name} not found in library {libname}")
                            return
                    else:
                        print(f"ERROR: Dataset {dataset_name} not found")
                        return
            else:
                # Use the most recently created dataset
                if self.data_sets:
                    dataset_name = list(self.data_sets.keys())[-1]
                    input_data = self.data_sets[dataset_name]
                else:
                    print("ERROR: No dataset available for PROC")
                    return
            
            # Execute the appropriate PROC
            if proc_info.proc_name in self.proc_implementations:
                proc_impl = self.proc_implementations[proc_info.proc_name]
                results = proc_impl.execute(input_data, proc_info)
                
                # Display output
                for line in results.get('output_text', []):
                    print(line)
                
                # Store output data if created
                if results.get('output_data') is not None:
                    if proc_info.output_option:
                        self.data_sets[proc_info.output_option] = results['output_data']
                    elif results.get('output_dataset'):
                        self.data_sets[results['output_dataset']] = results['output_data']
            else:
                print(f"ERROR: PROC {proc_info.proc_name} not implemented")
                
        except Exception as e:
            print(f"ERROR in PROC: {e}")
    
    def _execute_libname(self, statement: str) -> None:
        """Execute a LIBNAME statement."""
        print(f"Executing LIBNAME: {statement}")
        try:
            result = self.libname_manager.parse_libname_statement(statement)
            if result:
                libname, path = result
                if self.libname_manager.create_library(libname, path):
                    print(f"Library {libname} created and mapped to {path}")
                else:
                    print(f"ERROR: Could not create library {libname}")
            else:
                print(f"ERROR: Invalid LIBNAME statement: {statement}")
        except Exception as e:
            print(f"ERROR in LIBNAME: {e}")
    
    def _execute_let(self, statement: str) -> None:
        """Execute a %LET macro statement."""
        print(f"Executing %LET: {statement}")
        try:
            var_name, value = self.macro_parser.parse_let_statement(statement)
            self.macro_parser.macro_variables[var_name] = value
            print(f"Macro variable {var_name} = {value}")
        except Exception as e:
            print(f"ERROR in %LET: {e}")
    
    def get_data_set(self, name: str) -> Optional[pd.DataFrame]:
        """
        Get a data set by name.
        
        Args:
            name: Name of the data set
            
        Returns:
            DataFrame if found, None otherwise
        """
        return self.data_sets.get(name)
    
    def list_data_sets(self) -> List[str]:
        """List all available data sets."""
        return list(self.data_sets.keys())
    
    def clear_workspace(self) -> None:
        """Clear all data sets and reset the workspace."""
        self.data_sets.clear()
        self.libraries.clear()
        self.macro_variables.clear()
        self.options.clear()
