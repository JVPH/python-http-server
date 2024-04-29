import socket

response_codes = {
        "ok": "HTTP/1.1 200 OK",
        "not_found": "HTTP/1.1 404 Not Found"
}

def parse_request(data: str):
        lines = data.splitlines()
        

        method, path, version = lines[0].split(" ")
        _, user_agent = lines[2].split(" ")

        return { "method": method, "path": path, "version": version, "user_agent": user_agent }

def response_data(status: str, version: str, content_type: str = "text/plain", body: str = ""):
    crlf = "\r\n"
    response_status = f'{response_codes[status]}{crlf}'
    
    if status == "not_found" or body == "":
        response = f'{response_status}{crlf}'
    else:
        headers = f'Content-Type: {content_type}{crlf}Content-Length: {len(body)}{crlf}'
        response = f'{response_status}{headers}\n{body}{crlf}{crlf}'

    return response.encode()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept() # wait for client
    with conn:
        while True:
            data = conn.recv(1024).decode()
            print(data)
            parsed_data = parse_request(data) 
            print(parsed_data["path"]) 
            body = parsed_data["path"][len("/echo/"):]

            
            if not data: break       
            
            if parsed_data["path"].startswith("/echo/"):
                response = response_data("ok", parsed_data["version"], "text/plain", body)
            elif parsed_data["path"].startswith("/user-agent"):
                response = response_data("ok", parsed_data["version"], "text/plain", parsed_data["user_agent"])

                
            elif parsed_data["path"] == "/":
                response = response_data("ok", parsed_data["version"])
            else:
                response = response_data("not_found", parsed_data["version"])

            conn.sendall(response)

if __name__ == "__main__":
    main()

