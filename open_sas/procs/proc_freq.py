"""
PROC FREQ Implementation for Open-SAS

This module implements SAS PROC FREQ functionality for frequency
tables and cross-tabulations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from ..parser.proc_parser import ProcStatement


class ProcFreq:
    """Implementation of SAS PROC FREQ procedure."""
    
    def __init__(self):
        pass
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        """
        Execute PROC FREQ on the given data.
        
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
        
        # Get TABLES specification
        tables_spec = proc_info.options.get('tables', '')
        if not tables_spec:
            results['output_text'].append("ERROR: TABLES statement required for PROC FREQ.")
            return results
        
        # Parse tables specification
        # Handle options (everything after /)
        if '/' in tables_spec:
            table_part, options_part = tables_spec.split('/', 1)
            table_part = table_part.strip()
            options_part = options_part.strip()
        else:
            table_part = tables_spec.strip()
            options_part = ""
        
        # Parse table specification (variables)
        if '*' in table_part:
            # Two-way table
            vars_list = [var.strip() for var in table_part.split('*')]
            if len(vars_list) == 2:
                var1, var2 = vars_list
                if var1 in data.columns and var2 in data.columns:
                    results.update(self._create_crosstab(data, var1, var2, options_part))
                else:
                    results['output_text'].append(f"ERROR: Variables {var1} or {var2} not found in data.")
            else:
                results['output_text'].append("ERROR: Only two-way tables supported currently.")
        else:
            # One-way frequency
            var = table_part.strip()
            if var in data.columns:
                results.update(self._create_frequency_table(data, var, options_part))
            else:
                results['output_text'].append(f"ERROR: Variable {var} not found in data.")
        
        return results
    
    def _create_frequency_table(self, data: pd.DataFrame, var: str, options: str = "") -> Dict[str, Any]:
        """Create a one-way frequency table."""
        results = {
            'output_text': [],
            'output_data': None
        }
        
        # Calculate frequencies
        freq_table = data[var].value_counts().sort_index()
        total = len(data[var].dropna())
        
        results['output_text'].append(f"PROC FREQ - Frequency Table for {var}")
        results['output_text'].append("=" * 50)
        results['output_text'].append("")
        
        # Create formatted table
        lines = []
        lines.append(f"{'Value':<20} {'Frequency':<12} {'Percent':<10} {'Cumulative Percent':<18}")
        lines.append("-" * 60)
        
        cum_freq = 0
        for value, freq in freq_table.items():
            percent = (freq / total) * 100
            cum_freq += freq
            cum_percent = (cum_freq / total) * 100
            
            lines.append(f"{str(value):<20} {freq:<12} {percent:<10.1f} {cum_percent:<18.1f}")
        
        # Add total row
        lines.append("-" * 60)
        lines.append(f"{'Total':<20} {total:<12} {100.0:<10.1f} {100.0:<18.1f}")
        
        results['output_text'].extend(lines)
        
        # Create output DataFrame
        output_df = pd.DataFrame({
            'Value': freq_table.index,
            'Frequency': freq_table.values,
            'Percent': (freq_table.values / total) * 100
        })
        results['output_data'] = output_df
        
        return results
    
    def _create_crosstab(self, data: pd.DataFrame, var1: str, var2: str, options: str = "") -> Dict[str, Any]:
        """Create a two-way cross-tabulation table."""
        results = {
            'output_text': [],
            'output_data': None
        }
        
        # Parse options
        options_list = [opt.strip().lower() for opt in options.split()] if options else []
        nocol = 'nocol' in options_list
        nopercent = 'nopercent' in options_list
        
        # Create crosstab
        crosstab = pd.crosstab(data[var1], data[var2], margins=True, margins_name="Total")
        
        results['output_text'].append(f"PROC FREQ - Cross-tabulation: {var1} * {var2}")
        if options:
            results['output_text'].append(f"Options: {options}")
        results['output_text'].append("=" * 50)
        results['output_text'].append("")
        
        # Format crosstab for display
        lines = self._format_crosstab(crosstab, var1, var2, nocol, nopercent)
        results['output_text'].extend(lines)
        
        # Set output data
        results['output_data'] = crosstab
        
        return results
    
    def _format_crosstab(self, crosstab: pd.DataFrame, var1: str, var2: str, nocol: bool = False, nopercent: bool = False) -> List[str]:
        """Format crosstab DataFrame for display."""
        lines = []
        
        # Get column widths
        col_widths = {}
        for col in crosstab.columns:
            col_widths[col] = max(len(str(col)), crosstab[col].astype(str).str.len().max())
        
        # Create header
        header = f"{var1:<15} | " + " | ".join(f"{str(col):<{col_widths[col]}}" for col in crosstab.columns)
        lines.append(header)
        lines.append("-" * len(header))
        
        # Add rows
        for idx, row in crosstab.iterrows():
            row_str = f"{str(idx):<15} | " + " | ".join(f"{str(val):<{col_widths[col]}}" for col, val in zip(crosstab.columns, row))
            lines.append(row_str)
        
        # Add statistics if not suppressed
        if not nopercent:
            lines.append("")
            lines.append("Statistics:")
            total = crosstab.loc["Total", "Total"]
            for idx, row in crosstab.iterrows():
                if idx != "Total":
                    row_total = row["Total"]
                    row_percent = (row_total / total) * 100
                    lines.append(f"  {idx}: {row_total} ({row_percent:.1f}%)")
        
        return lines
