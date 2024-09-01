#!/usr/bin/env python3

# forcing a race condition between two threads;
# modification of an implementation found here: https://realpython.com/intro-to-python-threading/

import threading
import time

counter = 0

def increment():
    global counter
    for _ in range(10):
        temp = counter
        temp += 1
        time.sleep(0.1) # allow other thread to run
        counter = temp

t1 = threading.Thread(target=increment, args=())
t2 = threading.Thread(target=increment, args=())

t1.start()
t2.start()

t1.join()
t2.join()

print('Counter =', counter) # expecting 20
