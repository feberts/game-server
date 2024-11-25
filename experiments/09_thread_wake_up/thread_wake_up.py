#!/usr/bin/env python3
"""
Waking up a thread from within another thread.
"""

import threading
import time

event = threading.Event()

def func1():
    global event
    while True:
        event.clear()
        event.wait()
        print('func1() says hello')

def func2():
    global event
    while True:
        time.sleep(1)
        event.set()

threading.Thread(target=func1, args=(), daemon=True).start()
threading.Thread(target=func2, args=(), daemon=True).start()

time.sleep(10)
