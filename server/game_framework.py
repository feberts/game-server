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
import time # TODO needed?
import config # TODO needed?
import threading # TODO needed?
from tictactoe import TicTacToe

# TODO spell check of this whole file

class GameFramework:
    """
    Class GameFramework.
    
    This class manages active games and handles the interaction between clients and game instances.
    """
    def __init__(self):
        self._game_classes = [TicTacToe] # add each newly implemented game class here
        self._game_classes_by_name = {}
        self._active_games = {}

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

        handlers = {'start_game':self._start_game, 'join_game':self._join_game} # TODO add more handlers
        
        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')
        
        return handlers[request['type']](request)

    class _ActiveGame:
        """
        Wrapper class for game instances providing functionality for retrieving player IDs.
        """
        def __init__(self, game_instance, players):
            self.game = game_instance
            self._players_target = players
            self._next_id = 0
        _lock = threading.Lock()
        def get_id(self):# TODO atomic?
            with self._lock:
                ret = self._next_id
                self._next_id = self._next_id + 1
                return ret
        def ready(self):
            # ready when all players have joined
            return self._players_target == self._next_id

    def _start_game(self, request):
        """
        TODO
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str, 'players':int})
        if err: return utility.framework_error(err)
        
        game_name, token, players = request['game'], request['token'], request['players']
               
        # get game class:
        if game_name not in self._game_classes_by_name:
            return utility.framework_error('no such game')

        game_class = self._game_classes_by_name[game_name]
        
        # check number of players:
        if players > game_class.max_players() or players < game_class.min_players():
            return utility.framework_error('invalid number of players')
        
        # create game instance and add it to dictionary of active games:
        new_game = self._ActiveGame(game_class(players), players)
        self._active_games[(game_name, token)] = new_game

        # get player ID:
        player_id = new_game.get_id()

        # wait for others to join:
        seconds = 0
        
        while not new_game.ready() and seconds < config.timeout:
            time.sleep(1)
            seconds = seconds + 1

        if not new_game.ready():
            del self._active_games[(game_name, token)]
            return utility.framework_error('time out while waiting for others to join')

        return self._return_data({'player_id':player_id})
        
    def _retrieve_game(self, game, token):
        # check if game session exists:
        if game not in self._game_classes_by_name:
            return None, utility.framework_error('no such game')
        if (game, token) not in self._active_games:
            return None, utility.framework_error('no such game session')

        return self._active_games[(game, token)], None

    def _join_game(self, request):
        """
        TODO
        """
        # check and parse request:
        err = utility.check_dict(request, {'game':str, 'token':str})
        if err: return utility.framework_error(err)
        
        game_name, token = request['game'], request['token']
        
        # retrieve game:
        game, err = self._retrieve_game(game_name, token)
        if err:
            return err # no such game or game session
        if game.ready():
            return utility.framework_error('game is already full')

        # get player ID:
        player_id = game.get_id()

        # wait for others to join:
        seconds = 0
        
        while not game.ready() and seconds < config.timeout:
            time.sleep(1)
            seconds = seconds + 1

        if not game.ready():
            return utility.framework_error('time out while waiting for others to join')

        return self._return_data({'player_id':player_id})
        
    def _return_data(self, data):
        """
        TODO
        """
        return {'status':'ok', 'data':data}

