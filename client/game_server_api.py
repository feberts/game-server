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
    
    def start_game(self, server, port, game, players, token):
        """
        Start a game.

        This function asks the server to start a game. Other clients can use the join-function to join that game. To be able to join, they need to know the chosen token. The token is used, to identify the game session. It can be any string. This is a blocking function; the game starts as soon as the specified number of clients has joined the game. The function then returns the player ID. The server assigns IDs in the range 0..players-1 to all players that join the game.

        Parameters:
        server (str): Server IP
        port (int): port number
        game (str): name of the game
        players (int): total number of players
        token (str): name of the game session

        Returns:
        tuple(int, str):
            int: player ID, if the game was successfully started, else None
            str: error message, if a problem occurred, an empty string otherwise
        """
        self._server = server
        self._port = port
        self._game = game
        self._players = players 
        self._token = token




    _server = None # TODO funktioniert auch mit Domainnamen???
    _port = None
    _game = None
    _players = None
    _token = None
    _player_id = None
