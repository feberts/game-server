#!/usr/bin/env python3

# testing the python threading module after reading https://realpython.com/intro-to-python-threading/

import threading
import time

def thread_function(arg):
    for _ in range(5):
        print(arg)
        time.sleep(1)

print('Main programm starts')

t1 = threading.Thread(target=thread_function, args=('Thread 1',)) # args: list or tuple
t2 = threading.Thread(target=thread_function, args=('Thread 2',)) # daemon=True for daemon thread
# Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)

print('Starting thread 1')
t1.start()

print('Starting thread 2')
t2.start()

print('Waiting for threads to finish')
t1.join()
t2.join()

print('Main programm ends')

# - join() waits for both regular and daemon threads
# - daemon threads (daemon=True) are killed when the program ends or is killed
# - regular threads continue execution after the main program has ended
