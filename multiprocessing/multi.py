import multiprocessing
import time

def do_something(sleep):
    print(f'sleeping for {sleep} second...')
    time.sleep(sleep)
    print('done sleeping')

processes = []

if __name__ == '__main__':
    start = time.perf_counter()
    for _ in range(10):
        p = multiprocessing.Process(target=do_something, args=[1.5])   
        p.start()
        processes.append(p)
    for process in processes:
        process.join()

    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} second(s)')
