import concurrent.futures
import time

def do_something(sleep):
    print(f'sleeping for {sleep}s')
    time.sleep(sleep)
    return 'done sleeping'


if __name__ == '__main__':
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(do_something,x) for x in range(10)]
        
        for f in concurrent.futures.as_completed(results):
            print(f.result())

    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} second(s)')
