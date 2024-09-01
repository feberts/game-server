#!/usr/bin/env python3

# using a global variable as shared data in separate threads

import threading

counter = 0

def increment():
    global counter
    for _ in range(10):
        counter += 1

t1 = threading.Thread(target=increment, args=())
t2 = threading.Thread(target=increment, args=())

t1.start()
t2.start()

t1.join()
t2.join()

print('Counter =', counter)
