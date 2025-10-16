#!/usr/bin/env python3
"""
Notebook Runner for Open-SAS

This script is used by the VS Code extension to execute SAS code
in notebook environments and return structured results.
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add the Open-SAS package to the Python path
current_dir = Path(__file__).parent
open_sas_dir = current_dir.parent.parent / 'open_sas'
if open_sas_dir.exists():
    sys.path.insert(0, str(open_sas_dir.parent))

try:
    from open_sas.notebook_interpreter import NotebookSASInterpreter
except ImportError:
    print("ERROR: Open-SAS package not found. Please install it or check the path.")
    sys.exit(1)


def main():
    """Main entry point for the notebook runner."""
    parser = argparse.ArgumentParser(description='Execute SAS code for notebook')
    parser.add_argument('--code', required=True, help='SAS code to execute')
    parser.add_argument('--notebook', help='Notebook file path')
    
    args = parser.parse_args()
    
    try:
        # Create notebook interpreter
        interpreter = NotebookSASInterpreter()
        
        # Execute the SAS code
        result = interpreter.run_code(args.code)
        
        # Output result as JSON
        print(json.dumps(result, indent=2, default=str))
        
    except Exception as e:
        error_result = {
            'success': False,
            'output': '',
            'errors': f"Error executing SAS code: {e}",
            'datasets': {},
            'proc_results': [],
            'code': args.code
        }
        print(json.dumps(error_result, indent=2, default=str))
        sys.exit(1)


if __name__ == '__main__':
    main()
