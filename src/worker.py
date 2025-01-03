from dotenv import load_dotenv
from log import log
from os import environ
from threading import Thread
import json
import random
import socket
import time

load_dotenv()
dispatcher_address = ("0.0.0.0", int(environ.get("DISPATCHER_PORT")))

class Worker:

    def __init__(self):
        self.weight = random.randint(1, 100)
        self.actor = "WORKER"

    def run(self):
        self._register()
        self.threads = [
            Thread(target=self._heartbeat, daemon=False)
        ]
        for thread in self.threads:
            thread.start()
            thread.join()

    def _register(self):
        log(self.actor, f"Registering with dispatcher")
        retry_count = 0
        max_retries = 5
        while retry_count < max_retries:
            try:
                self.sock = socket.create_connection(address = dispatcher_address)
                self.sock.settimeout(5)
                message = json.dumps({
                    "type": "worker_register",
                    "weight": self.weight
                    }).encode()
                while True:
                    self.sock.send(message)
                    response = json.loads(self.sock.recv(1024).decode())
                    response_type = response["type"]
                    try:
                        if response_type == "worker_registered":
                            self.worker_id = response["worker_id"]
                            self.last_communication = time.time()
                            log(self.actor, f"Received id from dispatcher")
                            return     
                    except socket.timeout:
                        log(self.actor, f"Timeout, retrying...")
                        continue
            except ConnectionRefusedError:
                log(self.actor, f"Connection refused, retrying...")
                retry_count += 1
                time.sleep(2 * retry_count)  # Exponential backoff
            except Exception as e:
                log(self.actor, f"Error: {str(e)}")
                retry_count += 1
                time.sleep(2 * retry_count)
        self.sock.close()
        raise ConnectionError("WORKER | Failed to connect after maximum retries")
    
    def _heartbeat(self):
        number_of_failed_heartbeats = 0
        if self.sock:
            while True:
                message = json.dumps({
                    "type": "heartbeat",
                    "worker_id": self.worker_id
                    }).encode()
                self.sock.send(message)
                try:
                    response = json.loads(self.sock.recv(1024).decode())
                    response_type = response["type"]
                    if response_type == "heartbeat_response":
                        log(self.actor, f"Heartbeat acknowledged by dispatcher")
                        number_of_failed_heartbeats = 0
                    time.sleep(random.randint(10, 15))
                except socket.timeout:
                    if number_of_failed_heartbeats < 5:
                        log(self.actor, f"Heartbeat failed, retrying...")
                        number_of_failed_heartbeats += 1
                        continue
                    else:
                        log(self.actor, f"Maximum retries reached, shutting down")
                        self.sock.close()
                        return