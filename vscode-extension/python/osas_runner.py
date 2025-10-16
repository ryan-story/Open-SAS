#!/usr/bin/env python3
"""
Open-SAS Runner for VS Code Extension

This script is used by the VS Code extension to execute .osas files
using the Open-SAS interpreter.
"""

import sys
import os
import traceback
from pathlib import Path

# Add the Open-SAS package to the Python path
current_dir = Path(__file__).parent
open_sas_dir = current_dir.parent.parent / 'open_sas'
if open_sas_dir.exists():
    sys.path.insert(0, str(open_sas_dir.parent))

try:
    from open_sas import SASInterpreter
except ImportError:
    print("ERROR: Open-SAS package not found. Please install it or check the path.")
    sys.exit(1)


def main():
    """Main entry point for the runner."""
    if len(sys.argv) != 2:
        print("Usage: python osas_runner.py <file.osas>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"ERROR: File '{file_path}' not found.")
        sys.exit(1)
    
    if not file_path.endswith('.osas'):
        print(f"WARNING: File '{file_path}' does not have .osas extension.")
    
    try:
        # Create interpreter and run the file
        interpreter = SASInterpreter()
        interpreter.run_file(file_path)
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("Traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
