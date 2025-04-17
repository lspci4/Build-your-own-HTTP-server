import socket
import re
from threading import Thread

HOST = 'localhost'
PORT = 4221
BUFFER_SIZE = 1024

def request_user(data): 
    request_data = data.decode().splitlines()
    print(request_data) # [A,B,C,D] --> [0,1,2,3]
    
    request_line = request_data[0].split()
    path_user_agent = request_line[1]
    print(path_user_agent)
    
    if path_user_agent == '/':
        return '', 0
      
    elif path_user_agent.startswith('/echo/'):
        echo_text = path_user_agent[len('/echo/'):]
        return echo_text, len(echo_text) 
    
    elif path_user_agent=='/user-agent':    
        for line in request_data[1:]:
            if line.lower().startswith('user-agent'):
                parts = line.split(':', 1)
                user_agent = parts[1].strip()
                user_agent_len = len(user_agent)
                print(user_agent,user_agent_len)
        return user_agent, user_agent_len           
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

def handle_connection(conn, addr):
    print('Creando hilo..')
    with conn:
        print(f'Server listening on {HOST}:{PORT}')
        while True:              
            data = conn.recv(BUFFER_SIZE)
            if data:
                user_agent, user_agent_len = request_user(data)
                    
                if user_agent is not None:
                    http_response = response_user(user_agent,user_agent_len)
                    print(http_response.encode())
                    conn.sendall(http_response.encode())
                else:
                    http_response = response_404()
                    conn.sendall(http_response.encode())   

def path_user():
    print('Path a probar...')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        while True:
            conn, addr = s.accept()
            t = Thread(target=handle_connection, args=(conn, addr))
            t.daemon = True
            t.start()
        
        
if __name__=="__main__":
    main()