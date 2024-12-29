from os import environ
from dotenv import load_dotenv
import socket
import time

load_dotenv()
broadcast_address = (environ.get("BROADCAST_ADDRESS"), int(environ.get("BROADCAST_PORT")))

class Worker:

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            message = b"Hello There"
            print(f"Worker: sending '{message}' to {broadcast_address}")
            message_number = 0
            while True:
                message_number += 1
                message = f"Hello There {message_number}".encode()
                sock.sendto(message, broadcast_address)
                time.sleep(1)
        
        finally:
            print("Worker: closing the socket")
            sock.close()
