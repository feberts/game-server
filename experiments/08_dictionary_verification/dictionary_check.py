#!/usr/bin/env python3

"""
The idea is, to simplify verification of JSON data send by a client to the server.

One could omit all checks and access the dictionary in a try-except-block and then, if an exception is raised, perform an appropriate action. But the exception's error message would be of little use to a caller of an API function on the client side. The caller is not interested in what went wrong on the server, instead, he must be informed about why his use of the API function is not correct and what kind of arguments the function expects.

Before accessing the data, three things must be checked:

- is the argument of type dictionary?
- does the key you want to access exist?
- has its value the expected data type?
"""

def check_dict(d, expected):
    # if type(d) != dict:
        # return False, 'not a valid dictionary'

    for key_name, val_type in expected.items():
        # print(key_name, val_type)
        if key_name not in d:
            return False, f"keyword argument '{key_name}' of type {val_type} missing"
        if type(d[key_name]) != val_type:
            return False, f"data type of argument '{key_name}' must be {val_type}"

    return True, ''


def func(d):
    ok, msg = check_dict(d, {'a':str, 'b':int, 'c':float, 'd':bool, 'e':list, 'f':tuple, 'g':dict})

    if not ok:
        print(msg)
    else:
        print('okay')

d = {'a':'hallo', 'b':2, 'c':3.12, 'd':True, 'e':[1,2,3], 'f':(1,2), 'g':{'a':1,'b':2}}

func(d)
