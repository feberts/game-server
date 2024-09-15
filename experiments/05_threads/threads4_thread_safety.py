#!/usr/bin/env python3

# preventing race condition with a lock;
# modification of an example found here: https://realpython.com/intro-to-python-threading/

import threading
import time

class Counter:
    counter = 0
    _lock = threading.Lock()

    def increment(self):
        with self._lock: # ESSENTIAL PART !!!
            temp = self.counter
            temp += 1
            time.sleep(0.1) # allow other thread to run
            self.counter = temp

def increment():
    global counter
    for _ in range(10):
        counter.increment()

counter = Counter()

t1 = threading.Thread(target=increment, args=())
t2 = threading.Thread(target=increment, args=())

t1.start()
t2.start()

t1.join()
t2.join()

print('Counter =', counter.counter) # expecting 20
