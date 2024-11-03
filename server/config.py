"""
Server configuration.

This module contains configuration data for the server.
"""

# server:
ip = '127.0.0.1'
port = 4711

# connections:
buffer_size = 4096 # bytes
timeout = 30 # seconds
receive_size_max = int(1e6) # bytes
game_start_poll_interval = 0.1 # seconds

# logging:
log_server_errors = True
log_server_info = False
