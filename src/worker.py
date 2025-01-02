from os import environ
from dotenv import load_dotenv
import json
import random
import socket
import time

load_dotenv()
dispatcher_address = ("0.0.0.0", int(environ.get("DISPATCHER_PORT")))

class Worker:

    def __init__(self):
        self.weight = random.randint(1, 100)
        with socket.create_connection(dispatcher_address) as sock:
            print("Worker connected to dispatcher")
            message = json.dumps({
                "type": "is_someone_there",
                "weight": self.weight
                }).encode()
            while True:
                sock.send(message)
                time.sleep(5)
