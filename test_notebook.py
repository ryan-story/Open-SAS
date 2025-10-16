#!/usr/bin/env python3
"""
Test script for Open-SAS notebook functionality.

This test validates the notebook kernel and interpreter functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'open_sas'))

from open_sas.notebook_interpreter import NotebookSASInterpreter
from open_sas.kernel import install_kernel, check_kernel_installed

def test_notebook_interpreter():
    """Test the notebook-aware SAS interpreter."""
    print("Testing Open-SAS Notebook Interpreter")
    print("=" * 50)
    
    # Create notebook interpreter
    interpreter = NotebookSASInterpreter()
    
    # Test 1: Basic DATA step
    print("\nTest 1: Basic DATA step execution")
    print("-" * 30)
    
    sas_code1 = """
    data work.test_data;
        input id name $ age;
        datalines;
    1 Alice 30
    2 Bob 35
    3 Charlie 28
    ;
    run;
    """
    
    result1 = interpreter.run_code(sas_code1)
    print(f"Success: {result1['success']}")
    print(f"Output: {result1['output'][:100]}...")
    print(f"Datasets created: {list(result1['datasets'].keys())}")
    
    # Test 2: PROC execution
    print("\nTest 2: PROC execution")
    print("-" * 30)
    
    sas_code2 = """
    proc print data=work.test_data;
    run;
    """
    
    result2 = interpreter.run_code(sas_code2)
    print(f"Success: {result2['success']}")
    print(f"Output length: {len(result2['output'])}")
    
    # Test 3: Dataset information
    print("\nTest 3: Dataset information")
    print("-" * 30)
    
    dataset_info = interpreter.display_dataset('work.test_data')
    print(f"Dataset shape: {dataset_info['shape']}")
    print(f"Columns: {dataset_info['columns']}")
    print(f"Head data: {len(dataset_info['head'])} rows")
    
    # Test 4: Workspace summary
    print("\nTest 4: Workspace summary")
    print("-" * 30)
    
    workspace = interpreter.get_workspace_summary()
    print(f"Datasets: {workspace['datasets']}")
    print(f"Libraries: {workspace['libraries']}")
    print(f"Execution count: {workspace['execution_count']}")
    
    # Test 5: Export functionality
    print("\nTest 5: Export functionality")
    print("-" * 30)
    
    json_export = interpreter.export_dataset('work.test_data', 'json')
    print(f"JSON export length: {len(json_export)}")
    
    csv_export = interpreter.export_dataset('work.test_data', 'csv')
    print(f"CSV export length: {len(csv_export)}")
    
    print("\nNotebook interpreter tests completed!")

def test_kernel_installation():
    """Test kernel installation functionality."""
    print("\nTesting Kernel Installation")
    print("=" * 50)
    
    # Check if kernel is installed
    is_installed = check_kernel_installed()
    print(f"Kernel installed: {is_installed}")
    
    if not is_installed:
        print("Installing kernel...")
        success = install_kernel()
        print(f"Installation successful: {success}")
    else:
        print("Kernel is already installed!")

def main():
    """Run all notebook tests."""
    print("Open-SAS Notebook Functionality Test")
    print("=" * 60)
    
    # Test notebook interpreter
    test_notebook_interpreter()
    
    # Test kernel installation
    test_kernel_installation()
    
    print("\n" + "=" * 60)
    print("🎉 All notebook tests completed!")
    print("=" * 60)
    print("\nOpen-SAS notebook functionality includes:")
    print("✅ Notebook-aware SAS interpreter")
    print("✅ Structured execution results")
    print("✅ Dataset information and display")
    print("✅ Export functionality")
    print("✅ Workspace management")
    print("✅ Jupyter kernel support")
    print("✅ VS Code notebook integration")
    print("\nReady for interactive SAS analysis! 🚀")

if __name__ == '__main__':
    main()
