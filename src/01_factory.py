from concurrent import futures
from dispatcher import Dispatcher
from worker import Worker

def dispatcher():
    Dispatcher()

if __name__ == "__main__":
    with futures.ProcessPoolExecutor() as executor:
        executor.submit(dispatcher)
        executor.submit(Worker)
