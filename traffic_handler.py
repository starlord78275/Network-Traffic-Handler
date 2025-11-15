import socket
import threading
import json
import time
import hashlib
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

class TrafficHandler:
    def __init__(self, tcp_port=9999):
        self.tcp_port = tcp_port
        self.stats = {
            'total_bytes_received': 0,
            'total_bytes_sent': 0,
            'active_connections': 0,
            'total_connections': 0,
            'messages': [],
            'connected_clients': []
        }
        self.lock = threading.Lock()
    
    def websocket_handshake(self, client_socket, headers):
        """Perform WebSocket handshake"""
        try:
            key = None
            for line in headers.split('\r\n'):
                if 'Sec-WebSocket-Key' in line:
                    key = line.split(': ')[1].strip()
                    break
            
            if not key:
                return False
            
            magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            accept_key = base64.b64encode(
                hashlib.sha1((key + magic_string).encode()).digest()
            ).decode()
            
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n"
                "\r\n"
            )
            client_socket.send(response.encode())
            return True
        except:
            return False
    
    def decode_websocket_frame(self, data):
        """Decode WebSocket frame"""
        try:
            if len(data) < 2:
                return None
            
            payload_len = data[1] & 127
            
            if payload_len == 126:
                mask_start = 4
            elif payload_len == 127:
                mask_start = 10
            else:
                mask_start = 2
            
            mask = data[mask_start:mask_start+4]
            payload_start = mask_start + 4
            payload_data = data[payload_start:payload_start+payload_len]
            
            decoded = bytearray()
            for i in range(len(payload_data)):
                decoded.append(payload_data[i] ^ mask[i % 4])
            
            return decoded.decode('utf-8')
        except:
            return None
    
    def encode_websocket_frame(self, message):
        """Encode message as WebSocket frame"""
        message_bytes = message.encode('utf-8')
        frame = bytearray()
        frame.append(0x81)
        
        length = len(message_bytes)
        if length <= 125:
            frame.append(length)
        elif length <= 65535:
            frame.append(126)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(127)
            frame.extend(length.to_bytes(8, 'big'))
        
        frame.extend(message_bytes)
        return bytes(frame)
    
    def handle_websocket_client(self, client_socket, client_id):
        """Handle WebSocket connection"""
        print(f'[*] WebSocket connection established with {client_id}')
        
        try:
            while True:
                data = client_socket.recv(4096)
                if not data or len(data) == 0:
                    break
                
                # Check for close frame
                if data[0] & 0x08:
                    break
                
                message = self.decode_websocket_frame(data)
                if message:
                    with self.lock:
                        self.stats['total_bytes_received'] += len(message)
                        self.stats['messages'].append({
                            'from': client_id,
                            'message': message,
                            'time': time.strftime('%H:%M:%S'),
                            'timestamp': time.time()
                        })
                        if len(self.stats['messages']) > 100:
                            self.stats['messages'].pop(0)
                    
                    print(f'[MSG] {client_id}: {message}')
                    
                    response = f'ACK: {message}'
                    frame = self.encode_websocket_frame(response)
                    client_socket.send(frame)
                    
                    with self.lock:
                        self.stats['total_bytes_sent'] += len(response)
        except Exception as e:
            print(f'[!] WebSocket error with {client_id}: {e}')
    
    def handle_tcp_client(self, client_socket, client_id):
        """Handle regular TCP connection"""
        print(f'[*] Regular TCP connection from {client_id}')
        
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                if not message:
                    continue
                
                with self.lock:
                    self.stats['total_bytes_received'] += len(message)
                    self.stats['messages'].append({
                        'from': client_id,
                        'message': message,
                        'time': time.strftime('%H:%M:%S'),
                        'timestamp': time.time()
                    })
                    if len(self.stats['messages']) > 100:
                        self.stats['messages'].pop(0)
                
                print(f'[MSG] {client_id}: {message}')
                
                response = f'ACK: {message}'
                client_socket.send(response.encode('utf-8'))
                
                with self.lock:
                    self.stats['total_bytes_sent'] += len(response)
                    
        except Exception as e:
            print(f'[!] TCP error with {client_id}: {e}')
        
    def handle_client(self, client_socket, address):
        client_id = f'{address[0]}:{address[1]}'
        
        with self.lock:
            self.stats['active_connections'] += 1
            self.stats['total_connections'] += 1
            self.stats['connected_clients'].append(client_id)
            
        print(f'[+] Client connected: {client_id}')
        
        try:
            # Peek at first data to determine connection type
            client_socket.settimeout(1.0)
            first_data = client_socket.recv(4096, socket.MSG_PEEK)
            client_socket.settimeout(None)
            
            # Check if it's a WebSocket upgrade request
            if b'Upgrade: websocket' in first_data or b'Sec-WebSocket-Key' in first_data:
                # Read the full HTTP request
                http_request = client_socket.recv(4096).decode('utf-8', errors='ignore')
                print(f'[*] WebSocket handshake from {client_id}')
                
                if self.websocket_handshake(client_socket, http_request):
                    self.handle_websocket_client(client_socket, client_id)
                else:
                    print(f'[!] WebSocket handshake failed for {client_id}')
            else:
                # Regular TCP connection
                self.handle_tcp_client(client_socket, client_id)
                    
        except socket.timeout:
            print(f'[!] Timeout waiting for data from {client_id}')
        except Exception as e:
            print(f'[!] Error with {client_id}: {e}')
        finally:
            with self.lock:
                self.stats['active_connections'] -= 1
                if client_id in self.stats['connected_clients']:
                    self.stats['connected_clients'].remove(client_id)
            client_socket.close()
            print(f'[-] Client disconnected: {client_id}')
    
    def start_tcp_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.tcp_port))
        server.listen(10)
        print(f'[*] TCP/WebSocket Server listening on 0.0.0.0:{self.tcp_port}')
        
        while True:
            client, address = server.accept()
            client_thread = threading.Thread(
                target=self.handle_client, 
                args=(client, address),
                daemon=True
            )
            client_thread.start()

traffic_handler = TrafficHandler()

class WebHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        routes = {
            '/': ('text/html', 'index.html'),
            '/mobile_client.html': ('text/html', 'mobile_client.html'),
            '/style.css': ('text/css', 'style.css'),
            '/mobile_style.css': ('text/css', 'mobile_style.css'),
            '/app.js': ('application/javascript', 'app.js')
        }
        
        if parsed.path in routes:
            content_type, filename = routes[parsed.path]
            try:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, f'File not found: {filename}')
                
        elif parsed.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            with traffic_handler.lock:
                self.wfile.write(json.dumps(traffic_handler.stats).encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def start_web_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), WebHandler)
    local_ip = get_local_ip()
    
    print('\n' + '='*70)
    print('🚀 TRAFFIC HANDLER SERVER STARTED')
    print('='*70)
    print(f'📊 Dashboard:      http://{local_ip}:{port}')
    print(f'📱 Mobile Client:  http://{local_ip}:{port}/mobile_client.html')
    print(f'💻 Local Access:   http://localhost:{port}')
    print('='*70)
    print(f'\n✨ Server supports BOTH WebSocket (browsers) and TCP (Python client)!')
    print(f'📱 Phone: Use {local_ip}')
    print(f'💻 Desktop client: python traffic_client.py\n')
    
    server.serve_forever()

if __name__ == '__main__':
    tcp_thread = threading.Thread(target=traffic_handler.start_tcp_server, daemon=True)
    tcp_thread.start()
    start_web_server()
