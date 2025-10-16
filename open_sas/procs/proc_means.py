"""
PROC MEANS Implementation for Open-SAS

This module implements SAS PROC MEANS functionality using pandas
for descriptive statistics calculations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from ..parser.proc_parser import ProcStatement


class ProcMeans:
    """Implementation of SAS PROC MEANS procedure."""
    
    def __init__(self):
        pass
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        """
        Execute PROC MEANS on the given data.
        
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
        
        # Get analysis variables
        var_vars = proc_info.options.get('var', [])
        if not var_vars:
            # If no VAR specified, use all numeric columns
            var_vars = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Get BY variables
        by_vars = proc_info.options.get('by', [])
        
        # Filter to only include variables that exist in the data
        var_vars = [var for var in var_vars if var in data.columns]
        by_vars = [var for var in by_vars if var in data.columns]
        
        if not var_vars:
            results['output_text'].append("ERROR: No valid analysis variables found.")
            return results
        
        # Calculate statistics
        if by_vars:
            # Grouped analysis
            grouped = data.groupby(by_vars)
            stats_df = grouped[var_vars].agg(['count', 'mean', 'std', 'min', 'max'])
            
            # Flatten column names
            stats_df.columns = ['_'.join(col).strip() for col in stats_df.columns.values]
            stats_df = stats_df.reset_index()
            
            results['output_text'].append("PROC MEANS - Grouped Analysis")
            results['output_text'].append("=" * 50)
            
        else:
            # Overall analysis
            stats_dict = {}
            for var in var_vars:
                var_data = data[var].dropna()
                if len(var_data) > 0:
                    stats_dict[var] = {
                        'N': len(var_data),
                        'Mean': var_data.mean(),
                        'Std Dev': var_data.std(),
                        'Minimum': var_data.min(),
                        'Maximum': var_data.max()
                    }
            
            stats_df = pd.DataFrame(stats_dict).T
            stats_df = stats_df.round(6)
            
            results['output_text'].append("PROC MEANS - Descriptive Statistics")
            results['output_text'].append("=" * 50)
        
        # Format output
        results['output_text'].append(f"Analysis Variables: {', '.join(var_vars)}")
        if by_vars:
            results['output_text'].append(f"BY Variables: {', '.join(by_vars)}")
        results['output_text'].append("")
        
        # Convert DataFrame to formatted text
        output_lines = self._format_dataframe(stats_df)
        results['output_text'].extend(output_lines)
        
        # Set output data if requested
        if proc_info.output_option:
            results['output_data'] = stats_df
            results['output_dataset'] = proc_info.output_option
        
        return results
    
    def _format_dataframe(self, df: pd.DataFrame) -> List[str]:
        """Format DataFrame for text output."""
        lines = []
        
        # Get column widths
        col_widths = {}
        for col in df.columns:
            col_widths[col] = max(len(str(col)), df[col].astype(str).str.len().max())
        
        # Create header
        header = " | ".join(f"{col:<{col_widths[col]}}" for col in df.columns)
        lines.append(header)
        lines.append("-" * len(header))
        
        # Add rows
        for idx, row in df.iterrows():
            row_str = " | ".join(f"{str(val):<{col_widths[col]}}" for col, val in zip(df.columns, row))
            lines.append(row_str)
        
        return lines
