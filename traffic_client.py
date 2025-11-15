import socket

def send_traffic(host='127.0.0.1', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((host, port))
        print(f'[*] Connected to {host}:{port}')
        
        while True:
            message = input('Enter message (or "quit"): ')
            if message.lower() == 'quit':
                break
                
            client.send(message.encode('utf-8'))
            response = client.recv(1024)
            print(f'[*] Server: {response.decode("utf-8")}')
            
    except Exception as e:
        print(f'[!] Error: {e}')
    finally:
        client.close()
        print('[*] Disconnected')

if __name__ == '__main__':
    send_traffic()
