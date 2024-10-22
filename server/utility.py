"""
Utility functions.

This module provides various utility functions.
"""

def error_message(sender, message):
    """
    Create an error message.

    The message is embedded into a dictionary, to be sent back to the client.

    Parameters:
    sender (str): to let the client know, where the error occurred
    message (str): error message

    Returns:
    dict: contains the message
    """
    assert type(sender) == str and len(sender) > 0
    assert type(message) == str and len(message) > 0
    return {'status':'error', 'message':sender + ' error: ' + message}

def server_error(message):
    """
    Server error.

    See function error_message for details.
    """
    return error_message('server', message)

def check_dict(d, expected):
    """
    Checking a dictionary's structure.

    This function verifies, that all expected keys are present in a given dictionary and that their values are of the expected type.

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
