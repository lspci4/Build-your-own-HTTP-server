import socket
import re
from threading import Thread
import sys
import os

HOST = 'localhost'
PORT = 4221
BUFFER_SIZE = 1024

def request_user(data): 
    request_data = data.decode().splitlines()
    print(f'Request Data: {request_data} \r\n') # [A,B,C,D] --> [0,1,2,3]
    
    request_line = request_data[0].split()
    path_user = request_line[1]
    print(f'Path User: {path_user} \r\n')
    
    if path_user == '/':
        return '', 0
      
    elif path_user.startswith('/echo/'):
        echo_text = path_user[len('/echo/'):]
        return echo_text, len(echo_text) 
    
    elif path_user=='/user-agent':    
        for line in request_data[1:]:
            if line.lower().startswith('user-agent'):
                parts = line.split(':', 1)
                user_agent = parts[1].strip()
                user_agent_len = len(user_agent)
                print(f'user agent: {user_agent}, user agent len: {user_agent_len} \r\n')
        return user_agent, user_agent_len   
    elif path_user=='/files/':
        file_name = path_user[len('/files/'):]
        print(file_name)
        
        
    elif path_user.lower().startswith('/files/'):
        file_name = path_user[len('/files/'):]
        full_path = os.path.join(DIR_PATH, file_name)
        return full_path
    else:
        return None, None

def response_user(user_agent, user_agent_len):
    content = (
        f'HTTP/1.1 200 OK\r\n',
        f'Content-Type: text/plain\r\n',
        f'Content-Length: {user_agent_len}\r\n',
        f'\r\n',
        f'{user_agent}'
    )
    return ''.join(content)

def response_404():
    content = (
        f'HTTP/1.1 404 Not Found\r\n',
        f'Content-Type: text/plain\r\n',
        f'Content-Length: \r\n',
        f'\r\n',
        f'Not Found'
    )
    return ''.join(content)

def handle_connection(conn, addr,DIR_PATH):
    print('Creando hilo..')
    with conn:
        print(f'Server listening on {HOST}:{PORT}')
        while True:              
            data = conn.recv(BUFFER_SIZE)
            if data:
                user_agent, user_agent_len, DIR_PATH = request_user(data)
                    
                if user_agent is not None:
                    http_response = response_user(user_agent,user_agent_len)
                    print(http_response.encode())
                    conn.sendall(http_response.encode())
                else:
                    http_response = response_404()
                    conn.sendall(http_response.encode())   

def response_user_path():
    print('Path a probar...')

def main():
    ### python3 server.py --directory /tmp/
    ### sys.argv = ['server.py', '--directory', '/tmp']
    
    if len(sys.argv) ==3 and sys.argv[1] == '--directory':
        DIR_PATH = sys.argv[2]
        print(f'El directorio seleccionado es: {DIR_PATH}')
    else:
        print(f'Uso correcto: {sys.argv[0]} --directory <ruta>')
        exit(1)
        
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        while True:
            conn, addr = s.accept()
            t = Thread(target=handle_connection, args=(conn, addr, DIR_PATH))
            t.daemon = True
            t.start()
        
        
if __name__=="__main__":
    main()