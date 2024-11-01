"""
Game base class.TODO

This module provides a base class for games.TODO
"""

import threading

class GameSession: # TODO auslagern
    """
    Wrapper class for game instances providing functionality for retrieving player IDs.
    """
    def __init__(self, game_instance, players):
        self.game = game_instance
        self._number_of_players = players
        self._next_id = 0
        self._player_names = {} # player name -> ID
        self._lock = threading.Lock()

    def next_id(self, player_name): # IDs assigned to clients joining the game
        with self._lock:
            #TODO prüfen ob name schon vergeben
            # player ID:
            player_id = self._next_id
            self._next_id = self._next_id + 1
            # associate player name with ID:
            if player_name != '':
                self._player_names[player_name] = player_id
            return player_id

    def ready(self): # ready when all players have joined the game
        return self._number_of_players == self._next_id
    
    def player_id(self, player_name):#TODO kommentar TODO umbenennen
        if not player_name in self._player_names:
            return None, 'no such player'
        return self._player_names[player_name], None
