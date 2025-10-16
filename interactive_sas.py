#!/usr/bin/env python3
"""
Interactive SAS Runner for VS Code
This provides a cell-like experience for running SAS code
"""

from open_sas import SASInterpreter
import sys

class InteractiveSAS:
    def __init__(self):
        self.interpreter = SASInterpreter()
        self.cell_count = 0
    
    def run_cell(self, code):
        """Run a cell of SAS code"""
        self.cell_count += 1
        print(f"\n{'='*60}")
        print(f"CELL {self.cell_count}")
        print(f"{'='*60}")
        print(f"Code:\n{code.strip()}")
        print(f"\nOutput:")
        print("-" * 40)
        
        try:
            result = self.interpreter.run_code(code)
            if result:
                print(result)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 40)
        return result
    
    def show_datasets(self):
        """Show available datasets"""
        datasets = self.interpreter.list_data_sets()
        if datasets:
            print(f"\nAvailable datasets: {', '.join(datasets)}")
        else:
            print("\nNo datasets available")
    
    def show_libraries(self):
        """Show available libraries"""
        libraries = self.interpreter.libname_manager.list_libraries()
        if libraries:
            print(f"\nAvailable libraries: {', '.join(libraries)}")
        else:
            print("\nNo libraries available")

def main():
    """Interactive SAS session"""
    sas = InteractiveSAS()
    
    print("🧪 Interactive SAS Runner")
    print("=" * 60)
    print("Type SAS code and press Enter twice to execute")
    print("Commands:")
    print("  .datasets - Show available datasets")
    print("  .libraries - Show available libraries")
    print("  .quit - Exit")
    print("=" * 60)
    
    current_code = []
    
    while True:
        try:
            line = input("SAS> " if not current_code else "    ")
            
            if line.strip() == ".quit":
                break
            elif line.strip() == ".datasets":
                sas.show_datasets()
                continue
            elif line.strip() == ".libraries":
                sas.show_libraries()
                continue
            elif line.strip() == "":
                if current_code:
                    # Execute the accumulated code
                    code = "\n".join(current_code)
                    sas.run_cell(code)
                    current_code = []
                continue
            else:
                current_code.append(line)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
