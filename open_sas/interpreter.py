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
        # Remove comments and clean up code
        cleaned_code = self._clean_code(sas_code)
        
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
        # Split on semicolons, but be careful with semicolons in strings
        statements = []
        current_statement = ""
        in_string = False
        string_char = None
        
        for char in code:
            if char in ["'", '"'] and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif char == ';' and not in_string:
                statements.append(current_statement.strip())
                current_statement = ""
                continue
            
            current_statement += char
        
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
        # TODO: Implement DATA step parsing and execution
        # This would involve parsing the DATA statement, SET statements,
        # variable assignments, WHERE clauses, etc.
    
    def _execute_proc(self, statement: str) -> None:
        """Execute a PROC procedure."""
        print(f"Executing PROC: {statement}")
        # TODO: Implement PROC procedure parsing and execution
        # This would route to specific PROC implementations
    
    def _execute_libname(self, statement: str) -> None:
        """Execute a LIBNAME statement."""
        print(f"Executing LIBNAME: {statement}")
        # TODO: Implement LIBNAME functionality
    
    def _execute_let(self, statement: str) -> None:
        """Execute a %LET macro statement."""
        print(f"Executing %LET: {statement}")
        # TODO: Implement macro variable assignment
    
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
