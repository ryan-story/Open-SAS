"""
DATA Step Parser for Open-SAS

This module parses SAS DATA step syntax and converts it to executable
Python operations on DataFrames.
"""

import re
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DataStepStatement:
    """Represents a parsed DATA step statement."""
    type: str
    content: str
    line_number: int


@dataclass
class DataStepInfo:
    """Information about a DATA step."""
    output_dataset: str
    statements: List[DataStepStatement]
    set_datasets: List[str]
    where_conditions: List[str]
    variable_assignments: List[str]
    drop_vars: List[str]
    keep_vars: List[str]
    rename_vars: Dict[str, str]
    by_vars: List[str]


class DataStepParser:
    """Parser for SAS DATA step syntax."""
    
    def __init__(self):
        self.current_line = 0
        
    def parse_data_step(self, code: str) -> DataStepInfo:
        """
        Parse a complete DATA step.
        
        Args:
            code: The DATA step code to parse
            
        Returns:
            DataStepInfo object containing parsed information
        """
        lines = code.split('\n')
        statements = []
        
        # Find the DATA statement
        data_statement = None
        output_dataset = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            if line.upper().startswith('DATA '):
                data_statement = line
                # Extract output dataset name
                match = re.match(r'data\s+([^;]+)', line, re.IGNORECASE)
                if match:
                    output_dataset = match.group(1).strip()
                break
        
        if not data_statement:
            raise ValueError("No DATA statement found")
            
        # Parse remaining statements
        set_datasets = []
        where_conditions = []
        variable_assignments = []
        drop_vars = []
        keep_vars = []
        rename_vars = {}
        by_vars = []
        
        # First pass: combine multi-line assignments
        print(f"Starting multi-line parsing with {len(lines)} lines")
        combined_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.upper().startswith('DATA '):
                i += 1
                continue
                
            if line.upper() == 'RUN;':
                break
                
            # Check if this line starts an assignment that continues on next lines
            if '=' in line and not line.upper().startswith(('DROP', 'KEEP', 'RENAME', 'BY')):
                # Combine with following lines until we hit a semicolon or new statement
                combined_line = line
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line or next_line.upper() == 'RUN;':
                        break
                    if next_line.upper().startswith(('SET', 'WHERE', 'IF', 'DROP', 'KEEP', 'RENAME', 'BY')):
                        break
                    if '=' in next_line and not next_line.upper().startswith(('DROP', 'KEEP', 'RENAME', 'BY')):
                        # This is a new assignment, stop here
                        break
                    combined_line += ' ' + next_line
                    if ';' in next_line:
                        break
                    j += 1
                print(f"Combined line: {combined_line}")
                combined_lines.append(combined_line)
                i = j
            else:
                combined_lines.append(line)
                i += 1
        
        # Second pass: parse the combined lines
        for line in combined_lines:
            line = line.strip()
            if not line:
                continue
                
            # Parse SET statement
            if line.upper().startswith('SET '):
                set_match = re.match(r'set\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if set_match:
                    datasets = [ds.strip() for ds in set_match.group(1).split()]
                    set_datasets.extend(datasets)
                    
            # Parse WHERE statement
            elif line.upper().startswith('WHERE '):
                where_match = re.match(r'where\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if where_match:
                    where_conditions.append(where_match.group(1).strip())
                    
            # Parse IF/THEN/ELSE statements
            elif line.upper().startswith('IF '):
                # For now, treat as variable assignment
                variable_assignments.append(line)
                
            # Parse variable assignments
            elif '=' in line and not line.upper().startswith(('DROP', 'KEEP', 'RENAME', 'BY')):
                variable_assignments.append(line)
                
            # Parse DROP statement
            elif line.upper().startswith('DROP '):
                drop_match = re.match(r'drop\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if drop_match:
                    vars_list = [v.strip() for v in drop_match.group(1).split()]
                    drop_vars.extend(vars_list)
                    
            # Parse KEEP statement
            elif line.upper().startswith('KEEP '):
                keep_match = re.match(r'keep\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if keep_match:
                    vars_list = [v.strip() for v in keep_match.group(1).split()]
                    keep_vars.extend(vars_list)
                    
            # Parse RENAME statement
            elif line.upper().startswith('RENAME '):
                rename_match = re.match(r'rename\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if rename_match:
                    # Parse rename pairs like old=new
                    rename_pairs = rename_match.group(1).split()
                    for pair in rename_pairs:
                        if '=' in pair:
                            old, new = pair.split('=', 1)
                            rename_vars[old.strip()] = new.strip()
                            
            # Parse BY statement
            elif line.upper().startswith('BY '):
                by_match = re.match(r'by\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if by_match:
                    vars_list = [v.strip() for v in by_match.group(1).split()]
                    by_vars.extend(vars_list)
        
        # Debug: Print parsed assignments
        print(f"Parsed variable assignments: {variable_assignments}")
        
        return DataStepInfo(
            output_dataset=output_dataset,
            statements=statements,
            set_datasets=set_datasets,
            where_conditions=where_conditions,
            variable_assignments=variable_assignments,
            drop_vars=drop_vars,
            keep_vars=keep_vars,
            rename_vars=rename_vars,
            by_vars=by_vars
        )
    
    def parse_datalines(self, code: str) -> pd.DataFrame:
        """
        Parse DATALINES/CARDS section to create a DataFrame.
        
        Args:
            code: The DATALINES section code
            
        Returns:
            DataFrame created from the data
        """
        lines = code.split('\n')
        data_lines = []
        in_datalines = False
        input_statement = None
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith('INPUT '):
                # Remove semicolon if present
                if line.endswith(';'):
                    input_statement = line[:-1]
                else:
                    input_statement = line
                continue
            elif line.upper() in ['DATALINES;', 'CARDS;']:
                in_datalines = True
                continue
            elif line == ';' and in_datalines:
                break
            elif in_datalines and line:
                data_lines.append(line)
        
        if not data_lines or not input_statement:
            return pd.DataFrame()
            
        # Parse INPUT statement
        input_parts = input_statement[6:].strip().split()  # Remove 'INPUT '
        var_names = []
        var_types = {}
        
        i = 0
        while i < len(input_parts):
            part = input_parts[i]
            if i + 1 < len(input_parts) and input_parts[i + 1] == '$':
                # Character variable
                var_names.append(part)
                var_types[part] = 'str'
                i += 2  # Skip the $ token
            else:
                # Numeric variable
                var_names.append(part)
                var_types[part] = 'float'
                i += 1
        
        # Parse data lines
        data_rows = []
        for line in data_lines:
            values = line.split()
            if len(values) == len(var_names):
                row = {}
                for i, var_name in enumerate(var_names):
                    if var_types[var_name] == 'str':
                        row[var_name] = values[i]
                    else:
                        try:
                            row[var_name] = float(values[i])
                        except ValueError:
                            row[var_name] = None
                data_rows.append(row)
        
        return pd.DataFrame(data_rows)
