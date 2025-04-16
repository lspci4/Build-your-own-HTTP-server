import socket
import re

HOST = 'localhost'
PORT = 4221
BUFFER_SIZE = 1024

def request_user(data): 
    request_data = data.decode().splitlines()
    print(request_data) # [A,B,C,D] --> [0,1,2,3]
    
    request_line = request_data[0].split()
    path_user_agent = request_line[1]
    print(path_user_agent)
    
    if path_user_agent=='/user-agent':    
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

def response_404(user_agent, user_agent_len):
    content = (
        f'HTTP/1.1 404 Not Found\r\n',
        f'Content-Type: text/plain\r\n',
        f'Content-Length: {user_agent}\r\n',
        f'\r\n',
        f'Not Found'
    )
    return ''.join(content)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        
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
                        http_response = response_404(user_agent,user_agent_len)
                        conn.sendall(http_response.encode())
        
if __name__=="__main__":
    main()