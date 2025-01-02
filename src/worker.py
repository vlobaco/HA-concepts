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
        retry_count = 0
        max_retries = 5

        while retry_count < max_retries:
            try:
                with socket.create_connection(address = dispatcher_address) as sock:
                    sock.settimeout(5)
                    message = json.dumps({
                        "type": "is_someone_there",
                        "weight": self.weight
                        }).encode()
                    while True:
                        sock.send(message)
                        try:
                            response = json.loads(sock.recv(1024).decode())
                            if response["type"] == "worker_registered":
                                print(f"WORKER | Received id {response['id']} from dispatcher")
                                return
                        except socket.timeout:
                            print("Worker timed out, retrying...")
                            continue
            except ConnectionRefusedError:
                print(f"WORKER | Connection refused from address. Waiting before retry...")
                retry_count += 1
                time.sleep(2 * retry_count)  # Exponential backoff
            except Exception as e:
                print(f"WORKER | Error: {str(e)}")
                retry_count += 1
                time.sleep(2 * retry_count)
        raise ConnectionError("WORKER | Failed to connect after maximum retries")
