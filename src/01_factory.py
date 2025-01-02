from concurrent import futures
from dispatcher import Dispatcher
from worker import Worker

if __name__ == "__main__":
    with futures.ProcessPoolExecutor() as executor:
        executor.submit(Dispatcher)
        executor.submit(Worker)
        executor.submit(Worker)
        executor.submit(Worker)
        executor.submit(Worker)