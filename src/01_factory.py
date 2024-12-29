from dispatcher import Dispatcher
from worker import Worker
import threading
import time


def run_worker():
    Worker()

def run_dispatcher():
    Dispatcher()

if __name__ == "__main__":
    dispatcher_thread = threading.Thread(target=run_dispatcher)
    worker_thread = threading.Thread(target=run_worker)


    dispatcher_thread.start()
    time.sleep(1)
    worker_thread.start()

    dispatcher_thread.join()
    worker_thread.join()