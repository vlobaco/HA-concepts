from os import environ
from dotenv import load_dotenv
import socket

load_dotenv()
bind_address = ("0.0.0.0", int(environ.get("BROADCAST_PORT")))

class Dispatcher:

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(2)
        sock.bind(bind_address)

        try:
            while True:
                print("Dispatcher: waiting to receive")
                try:
                    data, server = sock.recvfrom(4096)
                except socket.timeout:
                    print('Dispatcher: Time out, no more responses')
                    break
                else:
                    print(f"Dispatcher: Received '{data}' from {server}")
        finally:
            print("Dispatcher: closing socket")
            sock.close()