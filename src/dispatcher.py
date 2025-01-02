from os import environ
from dotenv import load_dotenv
from time import time
import hashlib
import json
import selectors
import socket
import traceback

load_dotenv()
dispatcher_port = int(environ.get("DISPATCHER_PORT"))

class Dispatcher:

    def __init__(self):
        with socket.create_server(("", dispatcher_port)) as server:
            server.setblocking(False)  
            server.listen(5)
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
        data = client.recv(1024)
        if data:
            message = json.loads(data.decode())
            ip = client.getpeername()
            print(f"DISPATCHER | Received message {message['type']} from {ip}")
            
            response = json.dumps({
                "type": "worker_registered",
                "id": self._generate_hash(),
                }).encode()
            client.send(response)

    def _generate_hash(self):
        timestamp = str(round(time()*10000))
        hash_object = hashlib.md5(timestamp.encode())
        return hash_object.hexdigest()