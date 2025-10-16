#!/usr/bin/env python3
"""
Test script for LIBNAME functionality in Open-SAS.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'open_sas'))

from open_sas import SASInterpreter

def test_libname_functionality():
    """Test LIBNAME functionality."""
    print("Testing LIBNAME Functionality")
    print("=" * 50)
    
    # Create interpreter
    interpreter = SASInterpreter()
    
    # Test 1: Create a custom library
    print("\nTest 1: Creating custom library")
    print("-" * 30)
    
    sas_code1 = """
    libname mylib './test_data';
    """
    
    interpreter.run_code(sas_code1)
    
    # Test 2: Create dataset in custom library
    print("\nTest 2: Creating dataset in custom library")
    print("-" * 30)
    
    sas_code2 = """
    data mylib.sample_data;
        input name $ age height weight;
        datalines;
    John 25 70 180
    Mary 30 65 140
    Bob 35 72 200
    Alice 28 68 160
    ;
    run;
    """
    
    interpreter.run_code(sas_code2)
    
    # Test 3: Create dataset in WORK library
    print("\nTest 3: Creating dataset in WORK library")
    print("-" * 30)
    
    sas_code3 = """
    data work.temp_data;
        input id name $;
        datalines;
    1 Test1
    2 Test2
    3 Test3
    ;
    run;
    """
    
    interpreter.run_code(sas_code3)
    
    # Test 4: PROC PRINT from custom library
    print("\nTest 4: PROC PRINT from custom library")
    print("-" * 30)
    
    sas_code4 = """
    proc print data=mylib.sample_data;
    run;
    """
    
    interpreter.run_code(sas_code4)
    
    # Test 5: DATA step reading from custom library
    print("\nTest 5: DATA step reading from custom library")
    print("-" * 30)
    
    sas_code5 = """
    data work.filtered_data;
        set mylib.sample_data;
        where age > 30;
    run;
    """
    
    interpreter.run_code(sas_code5)
    
    # Test 6: PROC PRINT of filtered data
    print("\nTest 6: PROC PRINT of filtered data")
    print("-" * 30)
    
    sas_code6 = """
    proc print data=work.filtered_data;
    run;
    """
    
    interpreter.run_code(sas_code6)
    
    # Test 7: List libraries
    print("\nTest 7: List available libraries")
    print("-" * 30)
    
    libraries = interpreter.libname_manager.list_libraries()
    for libname, path in libraries.items():
        print(f"Library {libname}: {path}")
        datasets = interpreter.libname_manager.list_datasets(libname)
        print(f"  Datasets: {datasets}")
    
    print("\nAll LIBNAME tests completed!")

if __name__ == '__main__':
    test_libname_functionality()
