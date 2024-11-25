#!/usr/bin/env python3
"""
Test bench for client server interaction in separate threads. (This program has no specific purpose.)
"""

import threading
import time

a = 13

dummy_event = [threading.Event(), threading.Event()]

def condition():
    global a
    return a == 42

def func1():
    global dummy_event
    dummy_event[0].wait() 
    print('func1() says hello')

cond = threading.Condition()

def func2():

    global cond
    #with cond:
    cond.wait_for(condition)
    print('func2() says hello')


#threading.Thread(target=func1, args=(), daemon=True).start()

threading.Thread(target=func2, args=(), daemon=True).start()



time.sleep(1)
#dummy_event[0].set()
a = 42
time.sleep(1)
