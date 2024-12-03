"""
Utility.

This module provides various utility functions and classes.
"""

import config

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

def game_error(message):
    """
    Game error.

    See function generic_error() for details.
    """
    return generic_error('game', message)

def check_dict(d, expected):
    """
    Checking a dictionary's structure.

    This function verifies, that all expected keys are present in a given dictionary and that their values are of the expected type.

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

    return None

class ServerLogger:
    """
    Logging server information.

    The log level can be set in the config file. It is recommended to log errors only, as the info log is very verbose. It prints detailed information about every single connection and is only useful for debugging TCP connections.
    """
    def info(self, message, prefix=''):
        if config.log_server_info:
            self._log(message, prefix)

    def error(self, message, prefix=''):
        if config.log_server_errors:
            self._log(message, prefix)

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

    def _log(self, message, prefix):
        print(f'{prefix}[{self._ip}:{self._port}] {message}')

class FrameworkLogger:
    """
    Logging framework information.

    The log level can be set in the config file.
    """
    def info(self, message):
        """
        Logging actions initiated by the framework.

        Parameters:
        message (str): message
        """
        if config.log_framework_info:
            self._log(message)

    def request(self, request):
        """
        Logging client requests.

        Parameters:
        request (dict): client request
        """
        if config.log_framework_request:
            self._log(f'Request:  {request}')

    def response(self, response):
        """
        Logging server responses.

        Parameters:
        response (dict): server response
        """
        if config.log_framework_response:
            self._log(f'Response: {response}')

    def _log(self, message):
        print(message)
