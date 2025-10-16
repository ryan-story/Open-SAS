"""
PROC SORT Implementation for Open-SAS

This module implements SAS PROC SORT functionality for sorting
datasets by specified variables.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from ..parser.proc_parser import ProcStatement


class ProcSort:
    """Implementation of SAS PROC SORT procedure."""
    
    def __init__(self):
        pass
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        """
        Execute PROC SORT on the given data.
        
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
        
        # Get BY variables
        by_vars = proc_info.options.get('by', [])
        if not by_vars:
            results['output_text'].append("ERROR: BY statement required for PROC SORT.")
            return results
        
        # Filter to only include variables that exist in the data
        valid_by_vars = [var for var in by_vars if var in data.columns]
        if not valid_by_vars:
            results['output_text'].append("ERROR: No valid BY variables found in data.")
            return results
        
        # Check for NODUPKEY option
        nodupkey = proc_info.options.get('nodupkey', False)
        
        # Sort the data
        sorted_data = data.sort_values(by=valid_by_vars)
        
        # Handle NODUPKEY option
        if nodupkey:
            # Remove duplicate observations based on BY variables
            sorted_data = sorted_data.drop_duplicates(subset=valid_by_vars)
            results['output_text'].append(f"PROC SORT - Sorted with NODUPKEY option")
        else:
            results['output_text'].append("PROC SORT - Dataset Sorted")
        
        results['output_text'].append("=" * 50)
        results['output_text'].append(f"BY Variables: {', '.join(valid_by_vars)}")
        results['output_text'].append(f"Observations: {len(sorted_data)}")
        results['output_text'].append("")
        
        # Set output data
        results['output_data'] = sorted_data
        
        # Set output dataset name if specified
        if proc_info.output_option:
            results['output_dataset'] = proc_info.output_option
        
        return results
