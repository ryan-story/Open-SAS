#!/usr/bin/env python3
"""
Simple Open-SAS Jupyter Kernel
"""

import sys
import os
import json
import zmq
import uuid
import traceback
from datetime import datetime
from open_sas import SASInterpreter

# Add the open_sas package to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

class SimpleOSASKernel:
    """Simple Jupyter kernel for Open-SAS."""
    
    def __init__(self):
        self.interpreter = SASInterpreter()
        self.session_id = str(uuid.uuid4())
        self.execution_count = 0
        
    def run(self, connection_file):
        """Run the kernel with the given connection file."""
        # Read connection info
        with open(connection_file, 'r') as f:
            conn_info = json.load(f)
        
        # Create ZMQ context
        context = zmq.Context()
        
        # Create sockets
        shell_socket = context.socket(zmq.ROUTER)
        iopub_socket = context.socket(zmq.PUB)
        stdin_socket = context.socket(zmq.ROUTER)
        control_socket = context.socket(zmq.ROUTER)
        heartbeat_socket = context.socket(zmq.REP)
        
        # Bind sockets
        shell_socket.bind(f"tcp://{conn_info['ip']}:{conn_info['shell_port']}")
        iopub_socket.bind(f"tcp://{conn_info['ip']}:{conn_info['iopub_port']}")
        stdin_socket.bind(f"tcp://{conn_info['ip']}:{conn_info['stdin_port']}")
        control_socket.bind(f"tcp://{conn_info['ip']}:{conn_info['control_port']}")
        heartbeat_socket.bind(f"tcp://{conn_info['ip']}:{conn_info['hb_port']}")
        
        # Create poller
        poller = zmq.Poller()
        poller.register(shell_socket, zmq.POLLIN)
        poller.register(control_socket, zmq.POLLIN)
        poller.register(heartbeat_socket, zmq.POLLIN)
        
        print(f"Kernel started on {conn_info['ip']}:{conn_info['shell_port']}")
        
        try:
            while True:
                socks = dict(poller.poll(1000))
                
                # Handle heartbeat
                if heartbeat_socket in socks:
                    heartbeat_socket.recv()
                    heartbeat_socket.send(b'')
                
                # Handle shell messages
                if shell_socket in socks:
                    self._handle_shell_message(shell_socket, iopub_socket)
                
                # Handle control messages
                if control_socket in socks:
                    self._handle_control_message(control_socket, iopub_socket)
                    
        except KeyboardInterrupt:
            print("Kernel shutting down...")
        finally:
            # Clean up
            shell_socket.close()
            iopub_socket.close()
            stdin_socket.close()
            control_socket.close()
            heartbeat_socket.close()
            context.term()
    
    def _handle_shell_message(self, shell_socket, iopub_socket):
        """Handle a shell message."""
        try:
            # Receive message
            msg = shell_socket.recv_multipart()
            if len(msg) < 5:
                return
            
            # Parse message
            ident = msg[0]
            delimiter = msg[1]
            hmac = msg[2]
            header = json.loads(msg[3])
            parent_header = json.loads(msg[4])
            metadata = json.loads(msg[5]) if len(msg) > 5 else {}
            content = json.loads(msg[6]) if len(msg) > 6 else {}
            
            # Handle different message types
            msg_type = header['msg_type']
            
            if msg_type == 'execute_request':
                self._handle_execute_request(ident, header, parent_header, content, shell_socket, iopub_socket)
            elif msg_type == 'kernel_info_request':
                self._handle_kernel_info_request(ident, header, parent_header, shell_socket)
            elif msg_type == 'complete_request':
                self._handle_complete_request(ident, header, parent_header, content, shell_socket)
            elif msg_type == 'inspect_request':
                self._handle_inspect_request(ident, header, parent_header, content, shell_socket)
                
        except Exception as e:
            print(f"Error handling shell message: {e}")
            traceback.print_exc()
    
    def _handle_control_message(self, control_socket, iopub_socket):
        """Handle a control message."""
        try:
            # Receive message
            msg = control_socket.recv_multipart()
            if len(msg) < 5:
                return
            
            # Parse message
            ident = msg[0]
            delimiter = msg[1]
            hmac = msg[2]
            header = json.loads(msg[3])
            parent_header = json.loads(msg[4])
            metadata = json.loads(msg[5]) if len(msg) > 5 else {}
            content = json.loads(msg[6]) if len(msg) > 6 else {}
            
            # Handle different message types
            msg_type = header['msg_type']
            
            if msg_type == 'shutdown_request':
                self._handle_shutdown_request(ident, header, parent_header, content, control_socket)
                
        except Exception as e:
            print(f"Error handling control message: {e}")
            traceback.print_exc()
    
    def _handle_execute_request(self, ident, header, parent_header, content, shell_socket, iopub_socket):
        """Handle an execute request."""
        code = content.get('code', '')
        silent = content.get('silent', False)
        store_history = content.get('store_history', True)
        
        # Send status message
        if not silent:
            self._send_message(iopub_socket, 'status', {
                'execution_state': 'busy'
            }, parent_header)
        
        # Execute code
        try:
            if code.strip():
                # Execute SAS code
                result = self.interpreter.run_code(code)
                
                # Send output if any
                if hasattr(self.interpreter, 'last_output') and self.interpreter.last_output:
                    self._send_message(iopub_socket, 'stream', {
                        'name': 'stdout',
                        'text': self.interpreter.last_output
                    }, parent_header)
                
                # Send execution result
                self.execution_count += 1
                self._send_message(shell_socket, 'execute_reply', {
                    'status': 'ok',
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {}
                }, parent_header, ident)
            else:
                # Empty cell
                self._send_message(shell_socket, 'execute_reply', {
                    'status': 'ok',
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {}
                }, parent_header, ident)
                
        except Exception as e:
            # Send error
            self._send_message(iopub_socket, 'error', {
                'ename': 'SASError',
                'evalue': str(e),
                'traceback': [traceback.format_exc()]
            }, parent_header)
            
            self._send_message(shell_socket, 'execute_reply', {
                'status': 'error',
                'execution_count': self.execution_count,
                'ename': 'SASError',
                'evalue': str(e),
                'traceback': [traceback.format_exc()]
            }, parent_header, ident)
        
        # Send status message
        if not silent:
            self._send_message(iopub_socket, 'status', {
                'execution_state': 'idle'
            }, parent_header)
    
    def _handle_kernel_info_request(self, ident, header, parent_header, shell_socket):
        """Handle a kernel info request."""
        self._send_message(shell_socket, 'kernel_info_reply', {
            'protocol_version': '5.3',
            'implementation': 'Open-SAS',
            'implementation_version': '0.1.0',
            'language_info': {
                'name': 'sas',
                'version': '9.4',
                'mimetype': 'text/x-sas',
                'file_extension': '.osas',
                'pygments_lexer': 'sas',
                'codemirror_mode': 'sas'
            },
            'banner': 'Open-SAS Kernel - SAS alternative with Python backend'
        }, parent_header, ident)
    
    def _handle_complete_request(self, ident, header, parent_header, content, shell_socket):
        """Handle a complete request."""
        self._send_message(shell_socket, 'complete_reply', {
            'matches': [],
            'cursor_start': 0,
            'cursor_end': 0,
            'metadata': {},
            'status': 'ok'
        }, parent_header, ident)
    
    def _handle_inspect_request(self, ident, header, parent_header, content, shell_socket):
        """Handle an inspect request."""
        self._send_message(shell_socket, 'inspect_reply', {
            'status': 'ok',
            'data': {},
            'metadata': {}
        }, parent_header, ident)
    
    def _handle_shutdown_request(self, ident, header, parent_header, content, control_socket):
        """Handle a shutdown request."""
        self._send_message(control_socket, 'shutdown_reply', {
            'status': 'ok',
            'restart': content.get('restart', False)
        }, parent_header, ident)
    
    def _send_message(self, socket, msg_type, content, parent_header=None, ident=None):
        """Send a message."""
        header = {
            'msg_id': str(uuid.uuid4()),
            'username': 'kernel',
            'session': self.session_id,
            'date': datetime.now().isoformat(),
            'msg_type': msg_type,
            'version': '5.3'
        }
        
        if parent_header:
            header['parent_header'] = parent_header
        
        msg = [
            ident or b'',
            b'',
            b'',
            json.dumps(header).encode('utf-8'),
            json.dumps({}).encode('utf-8'),
            json.dumps({}).encode('utf-8'),
            json.dumps(content).encode('utf-8')
        ]
        
        socket.send_multipart(msg)


def main():
    """Main entry point."""
    if len(sys.argv) != 3 or sys.argv[1] != '-f':
        print("Usage: python simple_osas_kernel.py -f <connection_file>")
        sys.exit(1)
    
    connection_file = sys.argv[2]
    kernel = SimpleOSASKernel()
    kernel.run(connection_file)


if __name__ == '__main__':
    main()
