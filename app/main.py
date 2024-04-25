import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept() # wait for client
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data: break
            conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())



if __name__ == "__main__":
    main()
