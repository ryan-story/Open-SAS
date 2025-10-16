"""
PROC PRINT Implementation for Open-SAS

This module implements SAS PROC PRINT functionality for displaying
dataset contents.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from ..parser.proc_parser import ProcStatement


class ProcPrint:
    """Implementation of SAS PROC PRINT procedure."""
    
    def __init__(self):
        pass
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        """
        Execute PROC PRINT on the given data.
        
        Args:
            data: Input DataFrame
            proc_info: Parsed PROC statement information
            
        Returns:
            Dictionary containing results and output data
        """
        results = {
            'output_text': [],
            'output_data': None
        }
        
        display_data = data.copy()
        
        # Apply WHERE condition if present
        where_condition = proc_info.options.get('where', '')
        if where_condition:
            from ..utils.expression_parser import ExpressionParser
            from ..utils.data_utils import DataUtils
            expr_parser = ExpressionParser()
            data_utils = DataUtils()
            display_data = data_utils.apply_where_condition(display_data, where_condition, expr_parser)
        
        # Get VAR option for specific variables
        var_vars = proc_info.options.get('var', [])
        if var_vars:
            # Filter to only include variables that exist
            var_vars = [var for var in var_vars if var in display_data.columns]
            if var_vars:
                display_data = display_data[var_vars]
            else:
                results['output_text'].append("WARNING: No valid variables specified in VAR statement.")
        
        # Get OBS option for number of observations
        obs_limit = proc_info.options.get('obs', None)
        if obs_limit and isinstance(obs_limit, (int, str)):
            try:
                obs_limit = int(obs_limit)
                if obs_limit > 0:
                    display_data = display_data.head(obs_limit)
            except ValueError:
                pass
        
        results['output_text'].append("PROC PRINT - Dataset Contents")
        results['output_text'].append("=" * 50)
        results['output_text'].append(f"Observations: {len(display_data)}")
        results['output_text'].append(f"Variables: {len(display_data.columns)}")
        results['output_text'].append("")
        
        # Format the data for display
        if len(display_data) > 0:
            lines = self._format_dataframe(display_data)
            results['output_text'].extend(lines)
        else:
            results['output_text'].append("No observations to display.")
        
        return results
    
    def _format_dataframe(self, df: pd.DataFrame) -> List[str]:
        """Format DataFrame for display."""
        lines = []
        
        # Get column widths
        col_widths = {}
        for col in df.columns:
            col_widths[col] = max(len(str(col)), df[col].astype(str).str.len().max(), 8)
        
        # Create header
        header = " | ".join(f"{col:<{col_widths[col]}}" for col in df.columns)
        lines.append(header)
        lines.append("-" * len(header))
        
        # Add rows
        for idx, row in df.iterrows():
            row_str = " | ".join(f"{str(val):<{col_widths[col]}}" for col, val in zip(df.columns, row))
            lines.append(row_str)
        
        return lines
