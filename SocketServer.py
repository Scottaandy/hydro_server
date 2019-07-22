import socket
import select
import sys

class SocketServer:
    def __init__(self, host='0.0.0.0', port=12000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.inputs =[self.sock]

    def client_accept(self, server_sock):
        (client_sock, client_addr) = self.sock.accept()
        client_sock.setblocking(0)
        self.inputs.append(client_sock)

    def send_response(self, client_sock, text):
        client_sock.send("HTTP/1.1 200 OK\n".encode())
        client_sock.send("Content-Type: text/html\n\n".encode())
        client_sock.send(text.encode())

    def receive_request(self, client_sock):
        chunks = []
        chunk = ""
        done_reading = False
        while done_reading == False:
            try:
                chunk = client_sock.recv(50)
            except:
                done_reading = True;
            chunks.append(chunk)
        return chunks

    def close_client(self, client_sock):
        self.inputs.remove(client_sock)
        client_sock.close()

    def check_select(self):
        if self.inputs:
            readable, writable, exceptional = select.select(
                self.inputs, [], self.inputs,0)
            
            for s in readable:
                if s is self.sock:
                    self.client_accept(s)
                else:
                    data = self.receive_request(s)
                    return (data, s)

            for s in exceptional:
                self.inputs.remove(s)
                if s in outputs:
                    self.outputs.remove(s)
                s.close()
                