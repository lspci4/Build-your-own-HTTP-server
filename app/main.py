import socket
import re

host='localhost'
port=4221

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    print('Esperando conexión...')
    
    while True:
        conn, addr = s.accept()
        with conn:
            #print(f'\r\nRecibiendo conexión desde', addr)
            data = conn.recv(1024)
            request_data =data.decode().splitlines()
            request_line = request_data[0].split()
            
            request_path= re.search(r'^\/echo\/(.+)$', request_line[1])
                     
            
            if request_path:
                response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(request_path.group(1))}\r\n'
                '\r\n'
                f'{request_path.group(1)}')
                
                conn.sendall(response.encode())
            else:
                conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

        
        
        
