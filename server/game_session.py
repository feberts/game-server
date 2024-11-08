"""
Game session.

This module provides a class that contains all data associated with a specific game session.
"""

import threading
import time

class GameSession:
    """
    Class GameSession.
    
    This is a wrapper class for game instances providing functionality for retrieving player IDs.
    """
    def __init__(self, game_class, players):
        """
        Constructor.
        
        Instantiating a game class object and other attributes.
        
        Parameters:
        game_class (derived from AbstractGame): the game class
        players (int): number of players
        """
        self._game_class = game_class
        self._number_of_players = players
        self._game = game_class(players)
        self._next_id = 0
        self._player_names = {} # player name -> ID
        self._last_access = time.time()
        self._lock = threading.Lock()

    def next_id(self, player_name):
        """
        Returning a player ID.

        This function returns a new ID for each player joining a game session. If a none empty string is passed as the player name, this name together with the assigned ID will be added to a dictionary.

        Parameters:
        player_name (str): player name, can be an empty string

        Returns:
        int: the next player ID
        """
        with self._lock:
            # player ID:
            player_id = self._next_id
            self._next_id = self._next_id + 1
            
            # associate player name with ID:
            if player_name != '':
                self._player_names[player_name] = player_id
                
            return player_id

    def ready(self):
        """
        Game session is ready to start as soon as all players have joined the game.

        Returns:
        bool: True, if session ready, else False
        """
        return self._number_of_players == self._next_id
    
    def get_id(self, player_name):
        """
        Return player ID by name.
        
        This function returns the ID that was assigned to the passed player name.

        Parameters:
        player_name (str): name of an existing player that has already joined the game

        Returns:
        tuple(int, str):
            int: player ID, None in case of an error
            str: error message, if a problem occurred, None otherwise
        """
        if not player_name in self._player_names:
            return None, 'no such player'

        return self._player_names[player_name], None

    def get_game(self):
        """
        Return game instance and update time of last access.
        """
        self._last_access = time.time()
        return self._game

    def last_access(self):
        """
        Return time of last access.
        """
        return self._last_access

    def reset_game(self):
        """
        The game class object is replaced with a new instance.
        """
        self._game = self._game_class(self._number_of_players)
