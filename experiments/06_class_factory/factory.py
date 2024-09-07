#!/usr/bin/env python3

# implementing a method that creates objects by class name

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
    classes_by_name[type(cl()).__name__] = cl

def instantiate(name):
    return classes_by_name[name]()

cl = instantiate('DerivedA')
print(type(cl))
cl.override_me()
