#!/usr/bin/env python3
"""
Simple test kernel to verify VS Code communication
"""

import sys
import logging
from ipykernel.ipkernel import IPythonKernel

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/simple_kernel_debug.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('SimpleKernel')


class SimpleTestKernel(IPythonKernel):
    """Simple test kernel that just echoes input."""
    
    implementation = 'simple_test'
    implementation_version = '0.1.0'
    language = 'sas'
    language_version = '9.4'
    language_info = {
        'name': 'sas',
        'version': '9.4',
        'mimetype': 'text/x-sas',
        'file_extension': '.osas',
        'pygments_lexer': 'sas',
        'codemirror_mode': 'sas',
    }
    banner = "Simple Test Kernel - Echo SAS code"
    
    def __init__(self, **kwargs):
        logger.info("SimpleTestKernel initializing...")
        super().__init__(**kwargs)
        logger.info("SimpleTestKernel initialized successfully")
    
    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """Execute code by simply echoing it back."""
        
        logger.info(f"do_execute called with code: {repr(code)}")
        logger.info(f"silent={silent}, store_history={store_history}, allow_stdin={allow_stdin}")
        logger.info(f"execution_count: {self.execution_count}")
        
        # Skip empty cells
        if not code.strip():
            logger.info("Empty cell detected, returning ok status")
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }
        
        try:
            # Send a simple echo message
            if not silent:
                echo_msg = f"Echo: {code.strip()}"
                logger.info(f"Sending echo message: {echo_msg}")
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stdout',
                    'text': echo_msg + '\n'
                })
            
            logger.info("Returning successful execution result")
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }
            
        except Exception as e:
            logger.error(f"Exception during execution: {e}")
            
            # Send error to notebook
            if not silent:
                error_content = {
                    'ename': 'TestError',
                    'evalue': str(e),
                    'traceback': [str(e)]
                }
                self.send_response(self.iopub_socket, 'error', error_content)
            
            logger.info("Returning error execution result")
            return {
                'status': 'error',
                'execution_count': self.execution_count,
                'ename': 'TestError',
                'evalue': str(e),
                'traceback': [str(e)]
            }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SimpleTestKernel)
