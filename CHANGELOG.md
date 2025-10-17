# Changelog

All notable changes to Open-SAS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **PROC REG**: Linear regression analysis with MODEL, OUTPUT, and SCORE statements
- Comprehensive demo notebook (osas_walkthrough.ipynb)
- NOPRINT option support across all procedures
- Clean, professional output matching SAS behavior
- Proper column ordering in PROC MEANS OUTPUT statements
- Expression evaluator improvements for underscore variable names

### Fixed
- Expression evaluator underscore variable name handling
- PROC SORT ascending/descending order handling
- PROC FREQ TABLES statement parsing with options
- PROC MEANS OUTPUT dataset creation and display
- Automatic data printing issues in kernel
- Debug output cleanup for professional appearance

### Changed
- Major codebase cleanup and artifact removal
- Updated documentation and README
- Improved error handling and logging
- Enhanced SAS compatibility

## [0.1.0] - 2024-10-16

### Added
- Initial release of Open-SAS
- Core SAS interpreter with Python backend
- DATA step functionality with DATALINES support
- PROC MEANS with CLASS variables and OUTPUT statements
- PROC FREQ with cross-tabulations and options
- PROC SORT with ascending/descending order
- PROC PRINT for data display
- Jupyter notebook kernel support
- Macro variable support (%LET, %PUT)
- Library (LIBNAME) functionality
- Command line interface
- Comprehensive documentation

### Features
- SAS-like syntax for data manipulation
- Python pandas/numpy backend
- Cross-platform compatibility
- Clean, professional output
- Interactive notebook support
- Dataset visualization
- Error handling and reporting

## [0.0.1] - 2024-10-01

### Added
- Initial project setup
- Basic interpreter structure
- Core parsing framework
- Development environment setup
