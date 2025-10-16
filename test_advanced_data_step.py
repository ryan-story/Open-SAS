#!/usr/bin/env python3
"""
Test script for advanced DATA step features in Open-SAS.

This test demonstrates:
- IF/THEN/ELSE statements
- Variable assignments with expressions
- Complex data transformations
- SAS functions
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'open_sas'))

from open_sas import SASInterpreter

def test_advanced_data_step():
    """Test advanced DATA step features."""
    print("Testing Advanced DATA Step Features")
    print("=" * 50)
    
    # Create interpreter
    interpreter = SASInterpreter()
    
    # Test 1: Create base dataset
    print("\nTest 1: Creating base dataset")
    print("-" * 30)
    
    sas_code1 = """
    data work.employees;
        input emp_id name $ age salary department $;
        datalines;
    1 John 35 50000 Sales
    2 Mary 28 60000 IT
    3 Bob 42 75000 Sales
    4 Alice 31 55000 HR
    5 Charlie 29 65000 IT
    6 Diana 38 70000 Sales
    7 Edward 45 80000 IT
    8 Fiona 26 48000 HR
    ;
    run;
    """
    
    interpreter.run_code(sas_code1)
    
    # Test 2: IF/THEN/ELSE statements
    print("\nTest 2: IF/THEN/ELSE statements")
    print("-" * 30)
    
    sas_code2 = """
    data work.employee_analysis;
        set work.employees;
        if salary >= 60000 then salary_category = 'High';
        else salary_category = 'Standard';
        if age >= 40 then age_group = 'Senior';
        else if age >= 30 then age_group = 'Mid';
        else age_group = 'Junior';
    run;
    """
    
    interpreter.run_code(sas_code2)
    
    # Test 3: PROC PRINT of transformed data
    print("\nTest 3: PROC PRINT of transformed data")
    print("-" * 30)
    
    sas_code3 = """
    proc print data=work.employee_analysis;
    run;
    """
    
    interpreter.run_code(sas_code3)
    
    # Test 4: Variable assignments with expressions
    print("\nTest 4: Variable assignments with expressions")
    print("-" * 30)
    
    sas_code4 = """
    data work.employee_calculations;
        set work.employees;
        annual_bonus = salary * 0.1;
        total_compensation = salary + annual_bonus;
        salary_per_year_of_age = salary / age;
        is_high_earner = (salary > 60000);
    run;
    """
    
    interpreter.run_code(sas_code4)
    
    # Test 5: PROC PRINT of calculated data
    print("\nTest 5: PROC PRINT of calculated data")
    print("-" * 30)
    
    sas_code5 = """
    proc print data=work.employee_calculations;
    run;
    """
    
    interpreter.run_code(sas_code5)
    
    # Test 6: Complex conditional logic
    print("\nTest 6: Complex conditional logic")
    print("-" * 30)
    
    sas_code6 = """
    data work.employee_classification;
        set work.employees;
        if department = 'Sales' and salary >= 60000 then performance = 'Top Performer';
        else if department = 'IT' and age >= 35 then performance = 'Experienced';
        else if department = 'HR' then performance = 'Support';
        else performance = 'Standard';
        
        if salary >= 70000 then bonus_multiplier = 1.5;
        else if salary >= 60000 then bonus_multiplier = 1.2;
        else bonus_multiplier = 1.0;
        
        calculated_bonus = salary * bonus_multiplier * 0.1;
    run;
    """
    
    interpreter.run_code(sas_code6)
    
    # Test 7: PROC PRINT of classified data
    print("\nTest 7: PROC PRINT of classified data")
    print("-" * 30)
    
    sas_code7 = """
    proc print data=work.employee_classification;
    run;
    """
    
    interpreter.run_code(sas_code7)
    
    # Test 8: PROC FREQ on categorical variables
    print("\nTest 8: PROC FREQ on categorical variables")
    print("-" * 30)
    
    sas_code8 = """
    proc freq data=work.employee_classification;
        tables performance;
    run;
    """
    
    interpreter.run_code(sas_code8)
    
    print("\nAll advanced DATA step tests completed!")

if __name__ == '__main__':
    test_advanced_data_step()
