import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept() # wait for client
    with conn:
        while True:
            data = conn.recv(1024).decode().splitlines()
            http_method, path, http_version = data[0].split(" ")

            if not data: break
            
            response_codes = {
                "ok": "HTTP/1.1 200 OK\r\n\r\n",
                "not_found": "HTTP/1.1 404 Not Found\r\n\r\n"
            }
 
            if path == "/":
                conn.sendall(response_codes["ok"].encode())
            else:
               conn.sendall(response_codes["not_found"].encode())

if __name__ == "__main__":
    main()
