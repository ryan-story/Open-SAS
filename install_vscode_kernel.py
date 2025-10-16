#!/usr/bin/env python3
"""
Install Open-SAS kernel specifically for VS Code
This ensures VS Code can find and use the kernel
"""

import os
import json
import sys
import shutil
from pathlib import Path

def install_vscode_kernel():
    """Install Open-SAS kernel for VS Code compatibility."""
    
    # Get current Python executable
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    
    # Create kernel directory in user's Jupyter kernels
    kernel_dir = Path.home() / ".local" / "share" / "jupyter" / "kernels" / "osas"
    kernel_dir.mkdir(parents=True, exist_ok=True)
    
    # Create kernel.json with VS Code compatible settings
    kernel_spec = {
        "argv": [
            python_exe,
            "-m",
            "open_sas.kernel",
            "-f",
            "{connection_file}"
        ],
        "display_name": "Open-SAS",
        "language": "sas",
        "mimetype": "text/x-sas",
        "file_extension": ".osas",
        "codemirror_mode": "sas",
        "pygments_lexer": "sas",
        "interrupt_mode": "signal",
        "env": {},
        "metadata": {
            "debugger": False,
            "language_info": {
                "name": "sas",
                "mimetype": "text/x-sas",
                "file_extension": ".osas",
                "pygments_lexer": "sas",
                "codemirror_mode": "sas"
            }
        }
    }
    
    # Write kernel.json
    kernel_json_path = kernel_dir / "kernel.json"
    with open(kernel_json_path, 'w') as f:
        json.dump(kernel_spec, f, indent=2)
    
    print(f"✅ Kernel installed at: {kernel_dir}")
    print(f"✅ Kernel spec written to: {kernel_json_path}")
    
    # Also install in system location if possible
    try:
        system_kernel_dir = Path("/usr/local/share/jupyter/kernels/osas")
        system_kernel_dir.mkdir(parents=True, exist_ok=True)
        system_kernel_json = system_kernel_dir / "kernel.json"
        with open(system_kernel_json, 'w') as f:
            json.dump(kernel_spec, f, indent=2)
        print(f"✅ System kernel installed at: {system_kernel_dir}")
    except PermissionError:
        print("⚠️  Could not install system kernel (permission denied)")
    
    # Test kernel registration
    try:
        import jupyter_client
        kernels = jupyter_client.kernelspec.find_kernel_specs()
        if 'osas' in kernels:
            print("✅ Kernel successfully registered!")
            print(f"   Found at: {kernels['osas']}")
        else:
            print("❌ Kernel not found in registration")
    except Exception as e:
        print(f"❌ Error testing kernel registration: {e}")
    
    return kernel_dir

if __name__ == "__main__":
    install_vscode_kernel()
