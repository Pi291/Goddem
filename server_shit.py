import socket
HOST = "localhost"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server start on http:/{HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Get coneckted from:\n {client_address}") 

    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Get data:\n{request_data}")

    lines = request_data.splitlines()

    if request_data:
        request_line = lines[0]
        parts = request_line.split()

        if len(parts) >= 3:
            method, path, protocol = parts[0], parts[1], parts[2]
        else:
            method, path, protocol = '', '', ''

    else: 
        request_line = ''
        method, path, protocol = '', '', ''
        

    if path =='/':
        response_body = "<html><body><h1>Server working</h1></body></html>"
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Content_length: {len (response_body)}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "/r/n"
        )
        response = response_headers + response_body
    else:
        response_body = "<html><body><h1>Not Found</h1></body></html>"
        response_headers = (
            "HTTP/1.1 404 Not Found\r\n"
            f"Content_length: {len (response_body)}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "/r/n"
        )
        response = response_headers + response_body
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

server_socket.close()