import socket
import threading
from typing import Optional, Dict

class HTTPResponse:
    def __init__(self, status_code: int, reason_phrase: str, 
                 body: str = '', headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.body = body
        self.headers = headers or {}
        
        # Add default headers
        if 'Content-Length' not in self.headers:
            self.headers['Content-Length'] = str(len(body.encode('utf-8')))
        if 'Connection' not in self.headers:
            self.headers['Connection'] = 'keep-alive'  # HTTP/1.1 default
    
    def to_bytes(self) -> bytes:
        """Convert the response to bytes for sending over socket"""
        # Status line
        response_lines = [f"HTTP/1.1 {self.status_code} {self.reason_phrase}"]
        
        # Headers
        for key, value in self.headers.items():
            response_lines.append(f"{key}: {value}")
        
        # Empty line separating headers from body
        response_lines.append('')
        
        # Body
        response_lines.append(self.body)
        
        return '\r\n'.join(response_lines).encode('utf-8')
    
    def __repr__(self):
        return f"HTTPResponse(status_code={self.status_code}, reason_phrase={self.reason_phrase})"

class HTTPRequest:
    def __init__(self, method: str, path: str, version: str, 
                 headers: Dict[str, str], body: str = ''):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
    
    @classmethod
    def parse(cls, request_string: str) -> Optional['HTTPRequest']:
        """Parse a raw HTTP request string"""
        if not request_string:
            return None
        
        lines = request_string.split('\r\n')
        if len(lines) < 1:
            return None
        
        # Parse request line
        request_line_parts = lines[0].split(' ')
        if len(request_line_parts) != 3:
            return None
        
        method, path, version = request_line_parts
        
        # Parse headers
        headers = {}
        body_start_index = 1
        for i, line in enumerate(lines[1:], start=1):
            if line == '':  # Empty line indicates end of headers
                body_start_index = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        # Parse body
        body = '\r\n'.join(lines[body_start_index:]) if body_start_index < len(lines) else ''
        
        return cls(method, path, version, headers, body)
    
    def __repr__(self):
        return f"HTTPRequest(method={self.method}, path={self.path}, version={self.version})"

class HTTP11Server:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> TCP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        """Start the HTTP/1.1 server"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"HTTP/1.1 Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, address = self.socket.accept()
                print(f"Connection from {address}")
                # Handle each client in a separate thread for HTTP/1.1
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.socket.close()
    
    def handle_client(self, client_socket):
        """Handle a single client connection"""
        try:
            # HTTP/1.1 supports persistent connections
            while True:
                request_data = self.receive_request(client_socket)
                if not request_data:
                    break
                
                request = HTTPRequest.parse(request_data)
                if not request:
                    break
                
                response = self.handle_request(request)
                client_socket.sendall(response.to_bytes())
                
                # Check if connection should close
                if request.headers.get('Connection', '').lower() == 'close':
                    break
        finally:
            client_socket.close()
    
    def receive_request(self, client_socket):
        """Receive and parse HTTP request"""
        request_data = b''
        headers_complete = False
        content_length = 0
        
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            
            request_data += chunk
            
            if not headers_complete:
                # Check if headers are complete (double CRLF)
                if b'\r\n\r\n' in request_data:
                    headers_complete = True
                    header_end = request_data.index(b'\r\n\r\n') + 4
                    
                    # Parse content-length if present
                    headers_section = request_data[:header_end].decode('utf-8', errors='ignore')
                    for line in headers_section.split('\r\n'):
                        if line.lower().startswith('content-length:'):
                            content_length = int(line.split(':', 1)[1].strip())
                    
                    # Check if we have the full body
                    body_received = len(request_data) - header_end
                    if body_received >= content_length:
                        break
            else:
                # Continue receiving body
                header_end = request_data.index(b'\r\n\r\n') + 4
                body_received = len(request_data) - header_end
                if body_received >= content_length:
                    break
        
        return request_data.decode('utf-8', errors='ignore')
    
    def handle_request(self, request):
        """Process the request and generate a response"""
        # Simple routing
        if request.method == 'GET' and request.path == '/':
            return HTTPResponse(
                status_code=200,
                reason_phrase='OK',
                body='Hello from HTTP/1.1 Server!',
                headers={'Content-Type': 'text/plain'}
            )
        elif request.method == 'GET' and request.path == '/json':
            import json
            body = json.dumps({'message': 'Hello', 'protocol': 'HTTP/1.1'})
            return HTTPResponse(
                status_code=200,
                reason_phrase='OK',
                body=body,
                headers={'Content-Type': 'application/json'}
            )
        else:
            return HTTPResponse(
                status_code=404,
                reason_phrase='Not Found',
                body='404 - Not Found',
                headers={'Content-Type': 'text/plain'}
            )

if __name__ == '__main__':
    server = HTTP11Server(host='127.0.0.1', port=8080)
    server.start()