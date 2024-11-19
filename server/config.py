"""
Server configuration.

This module contains configuration data for the server.
"""

# server:
ip = '127.0.0.1'
port = 4711

# tcp connections:
buffer_size = 4096 # bytes
timeout = 30 # seconds
receive_size_max = int(1e6) # bytes
game_start_poll_interval = 0.1 # seconds # TODO an ort und stelle definieren

# logging:
log_server_info = False # useful only for debugging tcp connections (verbose)
log_server_errors = True # errors during tcp connections
log_framework_info = True # actions initiated by the framework
log_framework_request = True # client requests
log_framework_response = True # server responses

# TODO rm
log_framework_info = False
log_framework_request = False
log_framework_response = False
