from os import environ
from dotenv import load_dotenv
import json
import selectors
import socket

load_dotenv()
dispatcher_port = int(environ.get("DISPATCHER_PORT"))

class Dispatcher:

    def __init__(self):
        with socket.create_server(("", dispatcher_port)) as server:
            server.setblocking(False)
            server.listen(1)
            self.selector = selectors.DefaultSelector()
            self.selector.register(server, selectors.EVENT_READ, self._accept)
            print(f"Dispatcher listening on port {dispatcher_port}")
            while True:
                for key, mask in self.selector.select():
                    key.data(key.fileobj)

    def _accept(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self._read)

    def _read(self, client):
        message = json.loads(client.recv(1024).decode())
        ip = client.getpeername()
        print(f"DISPATCHER | Received message {message['type']} from {ip}")