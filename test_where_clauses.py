#!/usr/bin/env python3
"""
Test script for WHERE clause functionality in Open-SAS.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'open_sas'))

from open_sas import SASInterpreter

def test_where_clauses():
    """Test WHERE clause functionality."""
    print("Testing WHERE Clause Functionality")
    print("=" * 50)
    
    # Create interpreter
    interpreter = SASInterpreter()
    
    # Test 1: Create dataset with DATALINES
    print("\nTest 1: Creating dataset with DATALINES")
    print("-" * 30)
    
    sas_code1 = """
    data work.test_data;
        input name $ age height weight;
        datalines;
    John 25 70 180
    Mary 30 65 140
    Bob 35 72 200
    Alice 28 68 160
    Charlie 32 69 175
    ;
    run;
    """
    
    interpreter.run_code(sas_code1)
    
    # Test 2: PROC PRINT with WHERE clause
    print("\nTest 2: PROC PRINT with WHERE clause (age > 30)")
    print("-" * 30)
    
    sas_code2 = """
    proc print data=work.test_data;
        where age > 30;
    run;
    """
    
    interpreter.run_code(sas_code2)
    
    # Test 3: PROC PRINT with WHERE clause using macro variable
    print("\nTest 3: PROC PRINT with WHERE clause using macro variable")
    print("-" * 30)
    
    sas_code3 = """
    %let cutoff = 30;
    proc print data=work.test_data;
        where age > &cutoff;
    run;
    """
    
    interpreter.run_code(sas_code3)
    
    # Test 4: DATA step with WHERE clause
    print("\nTest 4: DATA step with WHERE clause")
    print("-" * 30)
    
    sas_code4 = """
    data work.filtered_data;
        set work.test_data;
        where age >= 30;
    run;
    """
    
    interpreter.run_code(sas_code4)
    
    # Test 5: PROC PRINT of filtered data
    print("\nTest 5: PROC PRINT of filtered data")
    print("-" * 30)
    
    sas_code5 = """
    proc print data=work.filtered_data;
    run;
    """
    
    interpreter.run_code(sas_code5)
    
    # Test 6: Complex WHERE condition
    print("\nTest 6: Complex WHERE condition (age > 25 and weight < 180)")
    print("-" * 30)
    
    sas_code6 = """
    proc print data=work.test_data;
        where age > 25 and weight < 180;
    run;
    """
    
    interpreter.run_code(sas_code6)
    
    print("\nAll WHERE clause tests completed!")

if __name__ == '__main__':
    test_where_clauses()
