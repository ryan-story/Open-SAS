#!/usr/bin/env python3
"""
Working Open-SAS Jupyter Kernel Launcher
"""

import sys
import os

# Add the open_sas package to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from open_sas.kernel.working_kernel import WorkingOSASKernel
from ipykernel.kernelapp import IPKernelApp

if __name__ == '__main__':
    # Create the app with our working kernel class
    app = IPKernelApp(kernel_class=WorkingOSASKernel)
    app.launch_instance()
