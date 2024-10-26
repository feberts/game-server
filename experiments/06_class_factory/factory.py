#!/usr/bin/env python3

# implementing a method that creates objects by class name

# Each time a client request the start of a new game, the server must create an object of the corresponding game class. It makes sense to have a mechanism that allows class instantiation by class name, since the clients are not aware of the game classes on the server and can only provide the game name as a string.

class Base:
    def override_me(self):
        raise NotImplementedError

class DerivedA(Base):
    def override_me(self):
        print('overridden by A')

class DerivedB(Base):
    def override_me(self):
        print('overridden by B')

classes = [DerivedA, DerivedB]
classes_by_name = {}

for cl in classes:
    #classes_by_name[type(cl()).__name__] = cl
    classes_by_name[cl.__name__] = cl

def instantiate(name):
    """factory method"""
    return classes_by_name[name]()

cl = instantiate('DerivedA')
print(type(cl))
cl.override_me()
