#!/usr/bin/env python3
"""
Basic test script for Open-SAS functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'open_sas'))

from open_sas import SASInterpreter

def test_basic_functionality():
    """Test basic Open-SAS functionality."""
    print("Testing Open-SAS Basic Functionality")
    print("=" * 50)
    
    # Create interpreter
    interpreter = SASInterpreter()
    
    # Test 1: Simple DATA step with DATALINES
    print("\nTest 1: DATA step with DATALINES")
    print("-" * 30)
    
    sas_code1 = """
    data work.test_data;
        input name $ age height weight;
        datalines;
    John 25 70 180
    Mary 30 65 140
    Bob 35 72 200
    Alice 28 68 160
    ;
    run;
    """
    
    interpreter.run_code(sas_code1)
    
    # Test 2: PROC PRINT
    print("\nTest 2: PROC PRINT")
    print("-" * 30)
    
    sas_code2 = """
    proc print data=work.test_data;
    run;
    """
    
    interpreter.run_code(sas_code2)
    
    # Test 3: PROC MEANS
    print("\nTest 3: PROC MEANS")
    print("-" * 30)
    
    sas_code3 = """
    proc means data=work.test_data;
        var age height weight;
    run;
    """
    
    interpreter.run_code(sas_code3)
    
    # Test 4: PROC FREQ
    print("\nTest 4: PROC FREQ")
    print("-" * 30)
    
    sas_code4 = """
    proc freq data=work.test_data;
        tables name;
    run;
    """
    
    interpreter.run_code(sas_code4)
    
    # Test 5: Macro variables
    print("\nTest 5: Macro Variables")
    print("-" * 30)
    
    sas_code5 = """
    %let cutoff = 30;
    proc print data=work.test_data;
        where age > &cutoff;
    run;
    """
    
    interpreter.run_code(sas_code5)
    
    print("\nAll tests completed!")

if __name__ == '__main__':
    test_basic_functionality()
