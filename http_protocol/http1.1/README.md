# HTTP/1.1 Protocol Implementation from Scratch

### Running the HTTP/1.1 Server

```bash
# Navigate to the HTTP/1.1 directory
cd http_protocol/http1.1

# Start the server
python server.py
```

You should see:
```
HTTP/1.1 Server listening on 127.0.0.1:8080
```

### Testing the Server

#### Using curl
```bash
# Basic GET request
curl http://localhost:8080/

# JSON endpoint
curl http://localhost:8080/json

# View full response with headers
curl -v http://localhost:8080/

# Test persistent connection
curl http://localhost:8080/ http://localhost:8080/json
```

#### Using a Web Browser
Simply open your browser and navigate to:
- http://localhost:8080/
- http://localhost:8080/json

#### Using Python requests
```python
import requests

response = requests.get('http://localhost:8080/')
print(response.text)  # "Hello from HTTP/1.1 Server!"

response = requests.get('http://localhost:8080/json')
print(response.json())  # {"message": "Hello", "protocol": "HTTP/1.1"}
```

## 🔍 How It Works

### The Architecture

```
Client (Browser/curl)
    ↓
    TCP Connection (3-way handshake)
    ↓
HTTP Request (text over TCP)
    ↓
┌─────────────────────────────────────┐
│  HTTP/1.1 Server                    │
│                                     │
│  1. Listen on TCP socket (port)     │
│  2. Accept incoming connections     │
│  3. Parse HTTP request              │
│     • Request line (GET /path)      │
│     • Headers                       │
│     • Body                          │
│  4. Route to handler                │
│  5. Generate HTTP response          │
│  6. Send response back              │
│  7. Keep connection alive or close  │
└─────────────────────────────────────┘
    ↓
HTTP Response (text over TCP)
    ↓
Client receives and displays
```

### Key Components

#### 1. TCP Socket Layer
```python
self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.socket.bind((host, port))
self.socket.listen(5)
```
- Creates a TCP socket (reliable, ordered delivery)
- Binds to IP address and port
- Listens for incoming connections

#### 2. HTTPRequest Parser
Parses raw HTTP requests following RFC 2616:
```http
GET /path HTTP/1.1\r\n
Host: localhost:8080\r\n
User-Agent: curl/7.64.1\r\n
\r\n
```

Into structured objects:
```python
HTTPRequest(
    method='GET',
    path='/path',
    version='HTTP/1.1',
    headers={'Host': 'localhost:8080', ...}
)
```

#### 3. HTTPResponse Builder
Creates properly formatted HTTP responses:
```python
HTTPResponse(
    status_code=200,
    reason_phrase='OK',
    body='Hello World',
    headers={'Content-Type': 'text/plain'}
)
```

Outputs:
```http
HTTP/1.1 200 OK\r\n
Content-Type: text/plain\r\n
Content-Length: 11\r\n
\r\n
Hello World
```

#### 4. Multi-threaded Connection Handling
Each client connection is handled in a separate thread, allowing multiple concurrent requests.

## 🎓 What You'll Learn

### Fundamental Concepts

1. **Sockets**: How programs communicate over networks
2. **TCP Protocol**: Reliable, connection-oriented communication
3. **HTTP Protocol**: Text-based request/response format
4. **Concurrency**: Threading for handling multiple clients
5. **Protocol Design**: Why protocols have specific formats

### HTTP/1.1 Specific Features

- **Text-based protocol**: Human-readable format
- **Persistent connections**: Reusing TCP connections (keep-alive)
- **Request/Response model**: Synchronous communication
- **Headers**: Metadata about requests/responses
- **Status codes**: 200 OK, 404 Not Found, etc.
- **Methods**: GET, POST, PUT, DELETE, etc.

## 🔧 API Reference

### HTTP11Server Class

#### Constructor
```python
server = HTTP11Server(host='127.0.0.1', port=8080)
```

**Parameters:**
- `host` (str): IP address to bind to (default: '127.0.0.1')
- `port` (int): Port number to listen on (default: 8080)

#### Methods

##### `start()`
Starts the HTTP server and begins listening for connections.
```python
server.start()  # Blocks until interrupted (Ctrl+C)
```

##### `handle_request(request)`
Override this method to implement custom routing:
```python
def custom_handler(self, request):
    if request.path == '/custom':
        return HTTPResponse(200, 'OK', body='Custom route!')
    return HTTPResponse(404, 'Not Found')
```

### HTTPRequest Class

**Attributes:**
- `method` (str): HTTP method (GET, POST, etc.)
- `path` (str): Request path (/index.html)
- `version` (str): HTTP version (HTTP/1.1)
- `headers` (dict): Request headers
- `body` (str): Request body

**Methods:**
- `parse(request_string)`: Class method to parse raw HTTP request

### HTTPResponse Class

**Attributes:**
- `status_code` (int): HTTP status code (200, 404, etc.)
- `reason_phrase` (str): Human-readable status (OK, Not Found)
- `body` (str): Response body
- `headers` (dict): Response headers

**Methods:**
- `to_bytes()`: Converts response to bytes for transmission

## 🛠️ Extending the Server

### Adding New Routes

Modify the `handle_request` method in `HTTP11Server`:

```python
def handle_request(self, request):
    if request.method == 'GET' and request.path == '/hello':
        return HTTPResponse(
            status_code=200,
            reason_phrase='OK',
            body='Hello, World!',
            headers={'Content-Type': 'text/plain'}
        )
    elif request.method == 'POST' and request.path == '/echo':
        # Echo back the request body
        return HTTPResponse(
            status_code=200,
            reason_phrase='OK',
            body=request.body,
            headers={'Content-Type': 'application/json'}
        )
    # ... add more routes
```


## This Project vs Flask

**This Project:**
```python
# server.py (201 lines)
server = HTTP11Server(host='127.0.0.1', port=8080)
server.start()
```

**Flask Equivalent:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from HTTP/1.1 Server!'

app.run(host='127.0.0.1', port=8080)
```
