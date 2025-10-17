#!/usr/bin/env python3
"""
Test script for Open-SAS v2.0 procedures
Tests all new statistical and ML procedures with sample data
"""

import pandas as pd
import numpy as np
from open_sas import SASInterpreter

def create_sample_data():
    """Create sample datasets for testing."""
    
    # Employee dataset for various analyses
    np.random.seed(42)
    n_employees = 100
    
    employees_data = {
        'employee_id': range(1, n_employees + 1),
        'name': [f'Employee_{i}' for i in range(1, n_employees + 1)],
        'department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR'], n_employees),
        'salary': np.random.normal(75000, 15000, n_employees).astype(int),
        'age': np.random.randint(22, 65, n_employees),
        'experience': np.random.randint(0, 20, n_employees),
        'performance_score': np.random.uniform(1, 10, n_employees),
        'satisfaction': np.random.choice(['Low', 'Medium', 'High'], n_employees),
        'remote': np.random.choice([0, 1], n_employees)
    }
    
    employees_df = pd.DataFrame(employees_data)
    
    # Time series data
    dates = pd.date_range('2020-01-01', periods=48, freq='M')
    sales_data = {
        'date': dates,
        'sales': 1000 + np.cumsum(np.random.normal(50, 100, 48)),
        'marketing_spend': np.random.normal(5000, 1000, 48),
        'seasonality': 100 * np.sin(2 * np.pi * np.arange(48) / 12)
    }
    
    sales_df = pd.DataFrame(sales_data)
    
    return employees_df, sales_df

def test_proc_univariate(interpreter, data):
    """Test PROC UNIVARIATE."""
    print("=" * 60)
    print("TESTING PROC UNIVARIATE")
    print("=" * 60)
    
    code = '''
    proc univariate data=work.employees;
        var salary age performance_score;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC UNIVARIATE: PASSED")
    except Exception as e:
        print(f"❌ PROC UNIVARIATE: FAILED - {e}")

def test_proc_corr(interpreter, data):
    """Test PROC CORR."""
    print("=" * 60)
    print("TESTING PROC CORR")
    print("=" * 60)
    
    code = '''
    proc corr data=work.employees;
        var salary age experience performance_score;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC CORR: PASSED")
    except Exception as e:
        print(f"❌ PROC CORR: FAILED - {e}")

def test_proc_factor(interpreter, data):
    """Test PROC FACTOR."""
    print("=" * 60)
    print("TESTING PROC FACTOR")
    print("=" * 60)
    
    code = '''
    proc factor data=work.employees method=pca nfactors=3;
        var salary age experience performance_score;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC FACTOR: PASSED")
    except Exception as e:
        print(f"❌ PROC FACTOR: FAILED - {e}")

def test_proc_cluster(interpreter, data):
    """Test PROC CLUSTER."""
    print("=" * 60)
    print("TESTING PROC CLUSTER")
    print("=" * 60)
    
    code = '''
    proc cluster data=work.employees method=kmeans nclusters=4;
        var salary age experience performance_score;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC CLUSTER: PASSED")
    except Exception as e:
        print(f"❌ PROC CLUSTER: FAILED - {e}")

def test_proc_npar1way(interpreter, data):
    """Test PROC NPAR1WAY."""
    print("=" * 60)
    print("TESTING PROC NPAR1WAY")
    print("=" * 60)
    
    code = '''
    proc npar1way data=work.employees;
        class department;
        var salary;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC NPAR1WAY: PASSED")
    except Exception as e:
        print(f"❌ PROC NPAR1WAY: FAILED - {e}")

def test_proc_ttest(interpreter, data):
    """Test PROC TTEST."""
    print("=" * 60)
    print("TESTING PROC TTEST")
    print("=" * 60)
    
    code = '''
    proc ttest data=work.employees;
        class remote;
        var salary;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC TTEST: PASSED")
    except Exception as e:
        print(f"❌ PROC TTEST: FAILED - {e}")

def test_proc_logit(interpreter, data):
    """Test PROC LOGIT."""
    print("=" * 60)
    print("TESTING PROC LOGIT")
    print("=" * 60)
    
    code = '''
    proc logit data=work.employees;
        model remote = salary age experience;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC LOGIT: PASSED")
    except Exception as e:
        print(f"❌ PROC LOGIT: FAILED - {e}")

def test_proc_freq_enhanced(interpreter, data):
    """Test enhanced PROC FREQ with Chi-square."""
    print("=" * 60)
    print("TESTING PROC FREQ (Enhanced with Chi-square)")
    print("=" * 60)
    
    code = '''
    proc freq data=work.employees;
        tables department*satisfaction / chisq;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC FREQ Enhanced: PASSED")
    except Exception as e:
        print(f"❌ PROC FREQ Enhanced: FAILED - {e}")

def test_proc_timeseries(interpreter, sales_data):
    """Test PROC TIMESERIES."""
    print("=" * 60)
    print("TESTING PROC TIMESERIES")
    print("=" * 60)
    
    # First create the sales data
    interpreter.run_code('''
    data work.sales;
        input date :yymmdd10. sales marketing_spend seasonality;
        format date yymmdd10.;
        datalines;
    2020-01-01 1000 5000 0
    2020-02-01 1100 5200 50
    2020-03-01 1200 4800 87
    2020-04-01 1300 5500 100
    2020-05-01 1250 5100 87
    2020-06-01 1400 5300 50
    2020-07-01 1350 4900 0
    2020-08-01 1500 5600 -50
    2020-09-01 1450 5200 -87
    2020-10-01 1600 5400 -100
    2020-11-01 1550 5000 -87
    2020-12-01 1700 5800 -50
    ;
    run;
    ''')
    
    code = '''
    proc timeseries data=work.sales type=decompose;
        var sales;
        time date;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC TIMESERIES: PASSED")
    except Exception as e:
        print(f"❌ PROC TIMESERIES: FAILED - {e}")

def test_proc_tree(interpreter, data):
    """Test PROC TREE."""
    print("=" * 60)
    print("TESTING PROC TREE")
    print("=" * 60)
    
    code = '''
    proc tree data=work.employees maxdepth=3;
        model satisfaction = salary age experience;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC TREE: PASSED")
    except Exception as e:
        print(f"❌ PROC TREE: FAILED - {e}")

def test_proc_forest(interpreter, data):
    """Test PROC FOREST."""
    print("=" * 60)
    print("TESTING PROC FOREST")
    print("=" * 60)
    
    code = '''
    proc forest data=work.employees ntrees=50;
        model satisfaction = salary age experience;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC FOREST: PASSED")
    except Exception as e:
        print(f"❌ PROC FOREST: FAILED - {e}")

def test_proc_boost(interpreter, data):
    """Test PROC BOOST."""
    print("=" * 60)
    print("TESTING PROC BOOST")
    print("=" * 60)
    
    code = '''
    proc boost data=work.employees ntrees=50 learningrate=0.1;
        model satisfaction = salary age experience;
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC BOOST: PASSED")
    except Exception as e:
        print(f"❌ PROC BOOST: FAILED - {e}")

def test_proc_language(interpreter, data):
    """Test PROC LANGUAGE (will fail if Ollama not running)."""
    print("=" * 60)
    print("TESTING PROC LANGUAGE")
    print("=" * 60)
    
    code = '''
    proc language model=llama2 mode=generate;
        prompt "What is the meaning of life?";
    run;
    '''
    
    try:
        interpreter.run_code(code)
        print("✅ PROC LANGUAGE: PASSED (or Ollama not running - expected)")
    except Exception as e:
        print(f"⚠️  PROC LANGUAGE: Expected failure (Ollama not running) - {e}")

def main():
    """Run all tests."""
    print("🚀 Open-SAS v2.0 Procedure Testing")
    print("=" * 60)
    
    # Create interpreter and sample data
    interpreter = SASInterpreter()
    employees_df, sales_df = create_sample_data()
    
    # Create employees dataset
    interpreter.run_code('''
    data work.employees;
        input employee_id name $ department $ salary age experience performance_score satisfaction $ remote;
        datalines;
    1 Employee_1 Engineering 75000 30 5 8.5 High 1
    2 Employee_2 Marketing 55000 25 2 7.2 Medium 0
    3 Employee_3 Sales 45000 28 3 6.8 Low 1
    4 Employee_4 Engineering 80000 35 8 9.1 High 0
    5 Employee_5 HR 60000 32 6 7.8 Medium 1
    6 Employee_6 Marketing 58000 27 4 8.0 High 0
    7 Employee_7 Sales 42000 24 1 6.5 Low 1
    8 Employee_8 Engineering 85000 40 12 9.5 High 0
    9 Employee_9 HR 62000 29 3 7.5 Medium 1
    10 Employee_10 Marketing 59000 31 7 8.2 High 0
    ;
    run;
    ''')
    
    # Run all tests
    test_proc_univariate(interpreter, employees_df)
    test_proc_corr(interpreter, employees_df)
    test_proc_factor(interpreter, employees_df)
    test_proc_cluster(interpreter, employees_df)
    test_proc_npar1way(interpreter, employees_df)
    test_proc_ttest(interpreter, employees_df)
    test_proc_logit(interpreter, employees_df)
    test_proc_freq_enhanced(interpreter, employees_df)
    test_proc_timeseries(interpreter, sales_df)
    test_proc_tree(interpreter, employees_df)
    test_proc_forest(interpreter, employees_df)
    test_proc_boost(interpreter, employees_df)
    test_proc_language(interpreter, employees_df)
    
    print("=" * 60)
    print("🎉 Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
