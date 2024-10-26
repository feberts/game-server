"""
Game framework.

This module implements the game framework. The framework is responsible for managing active games. It serves as an intermediary between the server and active game instances.

Client requests are parsed and the appropriate actions are performed. The following list shows the types of requests the framework can handle and the resulting actions:

- start: instantiate game class objects
- join: assign clients to games
- move: forward player moves to game instances
- state: report the game state to clients

To perform these actions, the framework calls the corresponding methods of a game class, if necessary.
"""

class GameFramework:
    """
    Class GameFramework.
    
    This class manages active games and handles the interaction between clients and game instances.
    """
    def __init__(self):
        pass

    def request(self, request):
        return {'status':'ok', 'message':'framework: no such game', 'data':{'player_id':13}}
