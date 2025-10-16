#!/usr/bin/env python3
"""
Standalone Open-SAS Jupyter Kernel
"""

import sys
import os

# Add the open_sas package to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from open_sas.kernel.osas_kernel import OSASKernel
from ipykernel.kernelapp import IPKernelApp

if __name__ == '__main__':
    # Create the app with our custom kernel class
    app = IPKernelApp(kernel_class=OSASKernel)
    app.launch_instance()
