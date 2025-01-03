from dispatcher import Dispatcher
from multiprocessing import Process
from worker import Worker

if __name__ == "__main__":
    number_of_workers = 10
    
    processes = [Process(target=Dispatcher().run)]
    processes.extend([Process(target=Worker().run) for _ in range(number_of_workers)])

    for process in processes:
         process.start()

    for process in processes:
        process.join()

    while True:
        pass