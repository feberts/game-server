"""
Utility functions.

This module provides utility functions for different purposes.
"""

def check_dict(d, expected):
    """
    Checking a dictionary's structure.

    This function verifies, that all expected keys are present in a given dictionary and that their values are of the expected data type.

    Example:
    To check, if dictionary d has keys named 'a' and 'b', that are mapped to values of types int and str, a function call might look like this:
    ok, msg = check_dict(d, {'a':int, 'b':str})

    Parameters:
    d (dict): dictionary to be checked
    expected (dict): contains the expected key names and value data types

    Returns:
    tuple(bool, str):
        bool: True, if dictionary has the expected structure, else False
        str: error message, if dictionary is okay, an empty string otherwise
    """
    for key_name, val_type in expected.items():
        if key_name not in d:
            return False, f"keyword argument '{key_name}' of type {val_type} missing"
        if type(d[key_name]) != val_type:
            return False, f"type of argument '{key_name}' must be {val_type}"

    return True, ''
