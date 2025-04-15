import socket

host='localhost'
port=4221

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print('Esperando conexión...')
    conn, addr = s.accept()
    with conn:
        print(f'Recibiendo conexión desde', addr)
        data = conn.recv(1024)
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
        print('Recibido:', repr(data))
