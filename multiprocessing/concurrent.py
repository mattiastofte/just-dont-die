import os
import multiprocessing

def square(number):
    result = number*number

    #process_id = os.getpid()
    #print(f'process is: {process_id}')

    process_name = multiprocessing.current_process().name
    print(f'current process name: {process_name}')
    print(f'the number {number} squares {result}')

if __name__ == '__main__':
    
    processes = []
    numbers = range(100)

    for number in numbers:
        process = multiprocessing.Process(target=square, args=(number,))
        # PROCESSES ARE SPAWNED BY CREATING A PROCESS OBJECT AND THEN CALLING ITS START() METHOD    
        process.start()