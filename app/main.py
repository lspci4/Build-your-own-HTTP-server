import socket

host='localhost'
port=4222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print('Esperando conexión...')
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f'Recibiendo conexión desde', addr)
            data = conn.recv(1024)
            print(data.decode())
            request_data =data.decode().splitlines()
            print(request_data)
            request_line = request_data[0].split()
            print(request_line)
            if request_line[1]=='/':
                conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            else:
                conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')

        
        
        
