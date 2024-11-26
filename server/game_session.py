"""
Game session.

This module provides a class that contains all data associated with a specific game session.
"""

import copy
import threading
import time

class GameSession:
    """
    Class GameSession.

    This is a wrapper class for game instances providing additional functionality.
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
        self._game_instance = game_class(players)
        self._next_id = 0
        self._player_names = {} # player name -> ID
        self._last_access = time.time()
        self._lock = threading.Lock()
        self._state_change = threading.Event()
        self._old_state = {} # player ID -> game state

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
            self._next_id += 1

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

        This function returns the ID that was assigned to the player.

        Parameters:
        player_name (str): name of an existing player that has already joined the game

        Returns:
        tuple(int, str):
            int: player ID, None if no such player exists
            str: error message, if a problem occurred, None otherwise
        """
        if not player_name in self._player_names:
            return None, 'no such player'

        return self._player_names[player_name], None

    def get_game(self):
        """
        Return game instance.
        """
        return self._game_instance

    def last_access(self):
        """
        Return time of last access.
        """
        return self._last_access

    def _touch(self):
        """
        Update time of last access.
        """
        self._last_access = time.time()

    def game_move(self, move, player_id):
        """
        Pass player's move to the game instance.
        """
        with self._lock:
            ret = self._game_instance.move(move, player_id)
            self._touch()
            self._state_change.set() # TODO
            return ret

    def game_state(self, player_id, blocking):
        """
        Retrieve game state from the game instance.
        """
        
        if blocking and not self._game_instance.game_over() and not player_id in self._game_instance.current_player(): # TODO
            self._state_change.clear() # TODO
            self._state_change.wait()
        if player_id in self._old_state: # TODO new
            ret = self._old_state[player_id]
            del self._old_state[player_id]
            return ret
            
        with self._lock:
            self._touch()
            return self._game_instance.state(player_id)

    def reset_game(self):
        """
        The game class object is replaced with a new instance.
        """
        if self._game_instance.game_over(): # TODO new
            for player_id in range(1, self._number_of_players):
                self._old_state[player_id] = copy.deepcopy(self._game_instance.state(player_id))
                self._old_state[player_id]['reset'] = True

        self._state_change.set() # TODO
        self._game_instance = self._game_class(self._number_of_players)
