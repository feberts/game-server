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

import utility
from tictactoe import TicTacToe

class GameFramework:
    """
    Class GameFramework.
    
    This class manages active games and handles the interaction between clients and game instances.
    """
    def __init__(self):
        self._game_classes = [TicTacToe] # add each newly implemented game here
        self._game_classes_by_name = {} # name -> class
        self._build_game_class_dict()

    def _build_game_class_dict(self):
        """
        Build dictionary mapping game names to game classes.
        """
        for game in self._game_classes:
            self._game_classes_by_name[game.__name__] = game

    def handle_request(self, request):
        """
        Handling a client request.

        This function is called by the server. It identifies the type of the request and redirects it to the corresponding method. The returned data is handed back to the server and then sent to the client.

        Parameters:
        request (dict): client request

        Returns:
        dict: reply
        """
        if 'type' not in request:
            return utility.framework_error("key 'type' of type str missing")

        handlers = {'start_game':self._start_game}
        
        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')
        
        return handlers[request['type']](request)

    def _start_game(self, request):
        """
        TODO
        """
        err = utility.check_dict(request, {'game':str, 'token':str, 'players':int})
        if err: return utility.framework_error(err)
    
        game, token, players = request['game'], request['token'], request['players']

        return {'status':'ok', 'data':{'player_id':13}}
        
        
