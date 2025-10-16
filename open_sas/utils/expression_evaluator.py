"""
Expression Evaluator for Open-SAS

This module provides functionality to evaluate SAS expressions
for variable assignments, IF/THEN/ELSE statements, and other
data step operations.
"""

import pandas as pd
import numpy as np
import re
from typing import Any, Dict, List, Union, Optional
from .expression_parser import ExpressionParser


class ExpressionEvaluator:
    """Evaluator for SAS expressions in DATA steps."""
    
    def __init__(self):
        self.expression_parser = ExpressionParser()
        
        # Define SAS functions
        self.functions = {
            'sum': lambda *args: sum(args),
            'mean': lambda *args: np.mean(args),
            'min': lambda *args: min(args),
            'max': lambda *args: max(args),
            'abs': abs,
            'sqrt': np.sqrt,
            'round': round,
            'int': int,
            'length': len,
            'substr': self._substr,
            'index': self._index,
            'compress': self._compress,
            'trim': str.strip,
            'upcase': str.upper,
            'lowcase': str.lower,
            'ifc': self._ifc,
            'ifn': self._ifn,
        }
    
    def evaluate_assignment(self, assignment: str, data: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate a variable assignment statement.
        
        Args:
            assignment: Assignment statement (e.g., "new_var = old_var * 2")
            data: DataFrame to apply the assignment to
            
        Returns:
            DataFrame with the new variable added
        """
        # Parse assignment: variable = expression
        match = re.match(r'(\w+)\s*=\s*(.+)', assignment.strip())
        if not match:
            return data
        
        var_name = match.group(1)
        expression = match.group(2).strip()
        
        try:
            # Evaluate the expression for each row
            result = self._evaluate_expression(expression, data)
            data[var_name] = result
            return data
        except Exception as e:
            print(f"Warning: Could not evaluate assignment '{assignment}': {e}")
            return data
    
    def evaluate_if_then_else(self, if_statement: str, data: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate an IF/THEN/ELSE statement.
        
        Args:
            if_statement: IF/THEN/ELSE statement
            data: DataFrame to apply the condition to
            
        Returns:
            DataFrame with conditional logic applied
        """
        # Parse IF/THEN/ELSE statement
        # Simple implementation for now
        if 'if' in if_statement.lower() and 'then' in if_statement.lower():
            # Extract condition and assignment
            match = re.match(r'if\s+(.+?)\s+then\s+(.+)', if_statement, re.IGNORECASE)
            if match:
                condition = match.group(1).strip()
                assignment = match.group(2).strip()
                
                # Parse assignment
                assign_match = re.match(r'(\w+)\s*=\s*(.+)', assignment)
                if assign_match:
                    var_name = assign_match.group(1)
                    value = assign_match.group(2).strip()
                    
                    # Create boolean mask for condition
                    mask = self.expression_parser.parse_where_condition(condition, data)
                    
                    # Apply conditional assignment
                    if var_name not in data.columns:
                        data[var_name] = None
                    
                    # Handle different value types
                    if value.startswith('"') and value.endswith('"'):
                        # String value
                        data.loc[mask, var_name] = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        # String value
                        data.loc[mask, var_name] = value[1:-1]
                    else:
                        # Try to evaluate as expression or numeric value
                        try:
                            if value.replace('.', '').replace('-', '').isdigit():
                                data.loc[mask, var_name] = float(value)
                            else:
                                # Try to evaluate as expression
                                result = self._evaluate_expression(value, data)
                                data.loc[mask, var_name] = result[mask]
                        except:
                            data.loc[mask, var_name] = value
        
        return data
    
    def _evaluate_expression(self, expression: str, data: pd.DataFrame) -> pd.Series:
        """
        Evaluate an expression for each row in the DataFrame.
        
        Args:
            expression: Expression to evaluate
            data: DataFrame to evaluate against
            
        Returns:
            Series with evaluated results
        """
        # Handle simple cases first
        if expression.strip() in data.columns:
            return data[expression.strip()]
        
        # Handle numeric literals
        if expression.replace('.', '').replace('-', '').isdigit():
            return pd.Series([float(expression)] * len(data), index=data.index)
        
        # Handle string literals
        if (expression.startswith('"') and expression.endswith('"')) or \
           (expression.startswith("'") and expression.endswith("'")):
            return pd.Series([expression[1:-1]] * len(data), index=data.index)
        
        # Handle arithmetic expressions
        if any(op in expression for op in ['+', '-', '*', '/', '**']):
            return self._evaluate_arithmetic(expression, data)
        
        # Handle function calls
        if '(' in expression and ')' in expression:
            return self._evaluate_function(expression, data)
        
        # Default: return as string
        return pd.Series([expression] * len(data), index=data.index)
    
    def _evaluate_arithmetic(self, expression: str, data: pd.DataFrame) -> pd.Series:
        """Evaluate arithmetic expressions."""
        try:
            # Replace column names with their values
            result = expression
            for col in data.columns:
                if col in expression:
                    # Replace column references with actual values
                    result = result.replace(col, f"data['{col}']")
            
            # Evaluate the expression
            return eval(result)
        except:
            # Fallback: return zeros
            return pd.Series([0] * len(data), index=data.index)
    
    def _evaluate_function(self, expression: str, data: pd.DataFrame) -> pd.Series:
        """Evaluate function calls."""
        # Parse function call: function_name(arg1, arg2, ...)
        match = re.match(r'(\w+)\s*\(([^)]+)\)', expression)
        if not match:
            return pd.Series([0] * len(data), index=data.index)
        
        func_name = match.group(1).lower()
        args_str = match.group(2)
        
        if func_name not in self.functions:
            return pd.Series([0] * len(data), index=data.index)
        
        # Parse arguments
        args = [arg.strip() for arg in args_str.split(',')]
        
        try:
            func = self.functions[func_name]
            
            # Evaluate arguments
            evaluated_args = []
            for arg in args:
                if arg in data.columns:
                    evaluated_args.append(data[arg])
                elif arg.replace('.', '').replace('-', '').isdigit():
                    evaluated_args.append(float(arg))
                elif (arg.startswith('"') and arg.endswith('"')) or \
                     (arg.startswith("'") and arg.endswith("'")):
                    evaluated_args.append(arg[1:-1])
                else:
                    evaluated_args.append(arg)
            
            # Apply function
            if len(evaluated_args) == 1 and isinstance(evaluated_args[0], pd.Series):
                return evaluated_args[0].apply(lambda x: func(x))
            else:
                return pd.Series([func(*evaluated_args)] * len(data), index=data.index)
                
        except:
            return pd.Series([0] * len(data), index=data.index)
    
    def _substr(self, string: str, start: int, length: int = None) -> str:
        """SAS SUBSTR function."""
        if length is None:
            return string[start-1:]
        return string[start-1:start-1+length]
    
    def _index(self, string: str, substring: str) -> int:
        """SAS INDEX function."""
        return string.find(substring) + 1 if substring in string else 0
    
    def _compress(self, string: str, chars: str = None) -> str:
        """SAS COMPRESS function."""
        if chars is None:
            return string.replace(' ', '')
        return ''.join(c for c in string if c not in chars)
    
    def _ifc(self, condition: bool, true_value: str, false_value: str) -> str:
        """SAS IFC function."""
        return true_value if condition else false_value
    
    def _ifn(self, condition: bool, true_value: float, false_value: float) -> float:
        """SAS IFN function."""
        return true_value if condition else false_value
