import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    
if __name__ == "__main__":
    main()
