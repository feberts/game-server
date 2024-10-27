"""
Utility functions.

This module provides various utility functions.
"""

def generic_error(sender, message):
    """
    Create an error message.

    The message is embedded into a dictionary, to be sent back to the client.

    Parameters:
    sender (str): to let the client know where the error was detected
    message (str): error message

    Returns:
    dict: contains the message
    """
    assert type(sender) == str and len(sender) > 0
    assert type(message) == str and len(message) > 0
    return {'status':'error', 'message':sender + ': ' + message}

def server_error(message):
    """
    Server error.

    See function generic_error() for details.
    """
    return generic_error('server', message)

def framework_error(message):
    """
    Framework error.

    See function generic_error() for details.
    """
    return generic_error('framework', message)

def check_dict(d, expected):
    """
    Checking a dictionary's structure.

    This function verifies, that all expected keys are present in a given dictionary and that their values are of the expected type. It also checks, if strings contain at least one character.

    Example: To check, if dictionary d has keys named 'a' and 'b', that are mapped to values of types int and str, a function call might look like this:

    d = {'a':42, 'b':'forty-two'}
    err = check_dict(d, {'a':int, 'b':str})
    if err: print(err)

    Parameters:
    d (dict): dictionary to be checked
    expected (dict): contains the expected key names and value data types

    Returns:
    str: None, if dictionary has the expected structure, an error message otherwise
    """
    for key_name, val_type in expected.items():
        if key_name not in d:
            return f"key '{key_name}' of type {val_type} missing"
        if type(d[key_name]) != val_type:
            return f"value of key '{key_name}' must be of type {val_type}"
        if type(d[key_name]) == str:
            if len(d[key_name]) == 0:
                return f"value of key '{key_name}' must be a string of length > 0"

    return None
