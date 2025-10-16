#!/usr/bin/env python3
"""
Simple script to test SAS code execution in VS Code
This can be used as a cell-like experience
"""

from open_sas import SASInterpreter

def run_sas_cell(code):
    """Run SAS code and return results"""
    interpreter = SASInterpreter()
    try:
        result = interpreter.run_code(code)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test cell 1: Create data
    print("=== Cell 1: Creating Sample Data ===")
    cell1 = """
    data work.sample;
        input name $ age salary;
        datalines;
    John 30 60000
    Mary 25 55000
    Bob 35 75000
    Alice 28 65000
    ;
    run;
    """
    result1 = run_sas_cell(cell1)
    print(result1)
    
    # Test cell 2: Display data
    print("\n=== Cell 2: Displaying Data ===")
    cell2 = """
    proc print data=work.sample;
    run;
    """
    result2 = run_sas_cell(cell2)
    print(result2)
    
    # Test cell 3: Statistics
    print("\n=== Cell 3: Calculating Statistics ===")
    cell3 = """
    proc means data=work.sample;
        var age salary;
    run;
    """
    result3 = run_sas_cell(cell3)
    print(result3)
    
    # Test cell 4: Filter with macro
    print("\n=== Cell 4: Filtering with Macro Variable ===")
    cell4 = """
    %let min_salary = 65000;
    
    proc print data=work.sample;
        where salary >= &min_salary;
    run;
    """
    result4 = run_sas_cell(cell4)
    print(result4)
