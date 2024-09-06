#!/usr/bin/env python3

class Base:
    def name(self):
        return 'Base'
    def override_me(self):
        raise NotImplementedError

class DerivedA(Base):
    def name(self):
        return 'DerivedA'
    def override_me(self):
        print('overwritten A')

class DerivedB(Base):
    def name(self):
        return 'DerivedB'
    def override_me(self):
        print('overwritten B')

classes = [DerivedA, DerivedB]
class_names = {}

for cl in classes:
    class_names[cl().name()] = cl

def class_factory(name):
    return class_names[name]()

derived_a = class_factory('DerivedA')
print(derived_a.name())
