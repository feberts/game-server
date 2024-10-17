"""
Game server API.

This module provides an API for communicating with the game server. The API can be used to

- start a game that other clients can join
- join a game that was started by another client
- submit moves to the server
- request the game state
"""

class GameServerAPI:
    """
    Class GameServerAPI.
    
    This class provides API functions to communicate with the game server.
    """
    
    def start_game(self, server, port, game, token, players):
        """
        Start a game.

        This function asks the server to start a game. Other clients can use the join-function to join that game. To be able to join, they need to know the chosen token. The token is used, to identify the game session. It can be any string. This is a blocking function; the game starts as soon as the specified number of clients has joined the game.

        Parameters:
        server (str): Server IP
        port (int): port number
        game (str): name of the game
        token (str): name of the game session
        players (int): total number of players

        Returns:
        tuple(bool, str):
            bool: True, if the game was successfully started, else False
            str: error message, if there is a problem, an empty string otherwise
        """
        pass
