"""
PROC Parser for Open-SAS

This module parses SAS PROC procedure syntax and extracts parameters
for execution by the appropriate PROC implementation.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ProcStatement:
    """Represents a parsed PROC statement."""
    proc_name: str
    options: Dict[str, Any]
    statements: List[str]
    data_option: Optional[str] = None
    output_option: Optional[str] = None


class ProcParser:
    """Parser for SAS PROC procedure syntax."""
    
    def __init__(self):
        pass
        
    def parse_proc(self, code: str) -> ProcStatement:
        """
        Parse a PROC procedure.
        
        Args:
            code: The PROC code to parse
            
        Returns:
            ProcStatement object containing parsed information
        """
        lines = code.split('\n')
        
        # Find the PROC statement
        proc_line = None
        proc_name = None
        data_option = None
        output_option = None
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith('PROC '):
                proc_line = line
                # Extract PROC name and options
                match = re.match(r'proc\s+(\w+)(?:\s+(.+?))?(?:\s*;)?$', line, re.IGNORECASE)
                if match:
                    proc_name = match.group(1).upper()
                    options_str = match.group(2) if match.group(2) else ""
                    
                    # Parse DATA= option
                    data_match = re.search(r'data\s*=\s*([\w.]+)', options_str, re.IGNORECASE)
                    if data_match:
                        data_option = data_match.group(1)
                        
                    # Parse OUT= option
                    out_match = re.search(r'out\s*=\s*(\w+)', options_str, re.IGNORECASE)
                    if out_match:
                        output_option = out_match.group(1)
                break
        
        # If no PROC line found, try to parse the first line as a combined PROC statement
        if not proc_line and lines:
            first_line = lines[0].strip()
            if first_line.upper().startswith('PROC '):
                proc_line = first_line
                # Extract PROC name and options
                match = re.match(r'proc\s+(\w+)(?:\s+(.+?))?(?:\s*;)?$', first_line, re.IGNORECASE)
                if match:
                    proc_name = match.group(1).upper()
                    options_str = match.group(2) if match.group(2) else ""
                    
                    # Parse DATA= option
                    data_match = re.search(r'data\s*=\s*([\w.]+)', options_str, re.IGNORECASE)
                    if data_match:
                        data_option = data_match.group(1)
                        
                    # Parse OUT= option
                    out_match = re.search(r'out\s*=\s*(\w+)', options_str, re.IGNORECASE)
                    if out_match:
                        output_option = out_match.group(1)
        
        if not proc_line:
            raise ValueError("No PROC statement found")
            
        # Parse remaining statements
        statements = []
        options = {}
        
        # Check if the PROC line contains additional statements
        if proc_line:
            # Extract TABLES statement from the PROC line
            if 'tables' in proc_line.lower():
                tables_match = re.search(r'tables\s+([^;]+)', proc_line, re.IGNORECASE)
                if tables_match:
                    options['tables'] = tables_match.group(1).strip()
            
            # Extract WHERE statement from the PROC line
            if 'where' in proc_line.lower():
                where_match = re.search(r'where\s+([^;]+)', proc_line, re.IGNORECASE)
                if where_match:
                    options['where'] = where_match.group(1).strip()
        
        for line in lines:
            line = line.strip()
            if not line or line.upper().startswith('PROC '):
                continue
                
            if line.upper() in ['RUN;', 'QUIT;']:
                break
                
            # Skip empty lines and comments
            if not line or line.startswith('*') or line.startswith('/*'):
                continue
                
            statements.append(line)
            
            # Parse common options
            if line.upper().startswith('VAR '):
                var_match = re.match(r'var\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if var_match:
                    options['var'] = [v.strip() for v in var_match.group(1).split()]
                    
            elif line.upper().startswith('BY '):
                by_match = re.match(r'by\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if by_match:
                    options['by'] = [v.strip() for v in by_match.group(1).split()]
                    
            elif line.upper().startswith('CLASS '):
                class_match = re.match(r'class\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if class_match:
                    options['class'] = [v.strip() for v in class_match.group(1).split()]
                    
            elif line.upper().startswith('TABLES '):
                tables_match = re.match(r'tables\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if tables_match:
                    options['tables'] = tables_match.group(1).strip()
                    
            elif line.upper().startswith('MODEL '):
                model_match = re.match(r'model\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if model_match:
                    options['model'] = model_match.group(1).strip()
                    
            elif line.upper().startswith('OUTPUT '):
                output_match = re.match(r'output\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if output_match:
                    options['output'] = output_match.group(1).strip()
                    
            elif line.upper().startswith('WHERE '):
                where_match = re.match(r'where\s+(.+?)(?:\s*;)?$', line, re.IGNORECASE)
                if where_match:
                    options['where'] = where_match.group(1).strip()
        
        # Debug: Print parsed options
        print(f"Parsed PROC options: {options}")
        print(f"Parsed statements: {statements}")
        
        return ProcStatement(
            proc_name=proc_name,
            options=options,
            statements=statements,
            data_option=data_option,
            output_option=output_option
        )
