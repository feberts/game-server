#!/usr/bin/env python3

"""
The idea is, to simplify verification of dictionaries passed to a function. Before accessing its data, three things must be checked:

- is the argument of type dictionary?
- does the key you want to access exist?
- has its value the expected data type?

One could omit all checks and access the dictionary in a try-except-block and then, if an exception is raised, perform an appropriate action, but the goal here is, to have a designated function for checking dictionaries. This allows for tidier code.
"""

d = {'a':'hallo', 'b':2, 'c':3.12, 'd':True, 'e':[1,2,3], 'f':(1,2), 'g':{'a':1,'b':2}}

expected = {'a':str, 'b':int, 'c':float, 'd':bool, 'e':list, 'f':tuple, 'g':dict}


if type(d) != dict:
    print('not a valid dictionary')
    exit()

for key_name, val_type in expected.items():
    #print(key_name, val_type)
    if key_name not in d:
        print(f"key '{key_name}' missing in dictionary")
        exit()
    if type(d[key_name]) != val_type:
        print(f"value of key '{key_name}' must be {val_type}")
        exit()
