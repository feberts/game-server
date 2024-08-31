#!/usr/bin/env python3


import threading
import time


def thread_function(arg):
    for _ in range(5):
        print(arg)
        time.sleep(1)

print('Main programm starts')

t1 = threading.Thread(target=thread_function, args=('Thread 1',))
t2 = threading.Thread(target=thread_function, args=('Thread 2',))

t1.start()
print('Thread 1 was started')

t2.start()
print('Thread 2 was started')

t1.join()
t2.join()

print('Main programm ends')
