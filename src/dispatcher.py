from threading import Thread
from os import environ
from dotenv import load_dotenv
from log import log
import hashlib
import json
import random
import selectors
import socket
import time

load_dotenv()
dispatcher_port = int(environ.get("DISPATCHER_PORT"))

class Dispatcher:
    def __init__(self):
        self.actor = "DISPATCHER"
        self.workers = {}

    def run(self):
        self.threads=[
            Thread(target=self._listen, daemon=False),
            Thread(target=self._cleanup, daemon=False),
        ]
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    def _listen(self):
        try:
            server = socket.create_server(("", dispatcher_port))
            log(self.actor, f"Listening on port {dispatcher_port}")
            self.workers = {}
            server.setblocking(False)  
            server.listen(5)
            self.selector = selectors.DefaultSelector()
            self.selector.register(server, selectors.EVENT_READ, self._accept)
            while True:
                for key, _ in self.selector.select():
                    key.data(key.fileobj)
        except Exception as e:
            log(self.actor, f"Error: {str(e)}")
        finally:
            log(self.actor, "Shutting down")

    def _accept(self, sock):
        conn, _ = sock.accept()
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, self._read)

    def _read(self, client):
        data = client.recv(1024)
        if data:
            message = json.loads(data.decode())
            ip = client.getpeername()
            type = message["type"]
            response = None
            if type == "worker_register":
                log(self.actor, f"Received register request from {ip}")
                worker_id = self._generate_hash()
                worker_weight = message["weight"]
                self.workers[worker_id] = {
                    "last_communication": time.time(),
                    "number_of_activations": 0,
                    "weight": worker_weight,
                    "ip": ip,
                    "id": worker_id
                }
                response = json.dumps({
                    "type": "worker_registered",
                    "worker_id": worker_id,
                    })
            elif type == "heartbeat":
                worker_id = message["worker_id"]
                if worker_id in self.workers:
                    log(self.actor, f"Received heartbeat from {ip}")
                    self.workers[worker_id]["last_communication"] = time.time()
                    response = json.dumps({
                        "type": "heartbeat_response",
                        "worker_id": worker_id
                        })
            if response:
                client.send(response.encode())

    def _generate_hash(self):
        timestamp = str(round(time.time()*10000))
        hash_object = hashlib.md5(timestamp.encode())
        return hash_object.hexdigest()
    
    def _cleanup(self):   
        try:
            while True:
                for worker in self.workers.copy().values():
                    if time.time() > 45:
                        log(self.actor, f"Worker {worker['ip']} has been inactive for too long, removing")
                        del self.workers[worker["id"]]
                time.sleep(1)
        except Exception as e:
            log(self.actor, f"Error: {str(e)}")