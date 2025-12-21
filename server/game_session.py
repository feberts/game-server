"""
Game session.

This module provides a class that handles a single game session.
"""

import copy
import random
import string
import threading
import time

class GameSession:
    """
    Class GameSession.

    This class contains a game instance and all data associated with the
    specific game session. It assigns player IDs, passes requests like player
    moves to the game instance, and provides the framework with information
    about the game session.
    """

    def __init__(self, game_class, players):
        """
        Instantiating a game class object and initializing other attributes.

        Parameters:
        game_class (derived from AbstractGame): the game class itself, not an instance
        players (int): number of players
        """
        self._game_class = game_class
        self._n_players = players
        self._game = None
        self._next_id = 0
        self._player_ids = {} # player name -> ID
        self._passwords = {} # player ID -> password
        self._last_access = time.time()
        self._lock = threading.Lock()
        self._state_change = threading.Event()
        self._no_delay = [] # IDs, players will receive the state immediately
        self._in_previous_game = [] # IDs, after restart, receive state of previous game once
        self._previous_game = None # previous game instance stored upon restart
        self._new_game()
        self._timed_out = False

    def next_id(self, player_name):
        """
        Returning a player ID and a password.

        This function returns a new ID and a password for each player joining a
        game session. If a none empty string is passed as the player name, this
        name together with the assigned ID is added to a dictionary.

        Parameters:
        player_name (str): player name, can be an empty string

        Returns:
        tuple(int, str, str):
            int: the next player ID
            str: a generated password
            str: error message, if a problem occurred, None otherwise
        """
        with self._lock:
            if player_name in self._player_ids:
                return None, None, 'name already in use'

            # player ID:
            player_id = self._next_id
            self._next_id += 1

            # associate player name with ID:
            if player_name != '':
                self._player_ids[player_name] = player_id

            # generate password:
            password = self._password()
            self._passwords[player_id] = password

            return player_id, password, None

    def full(self):
        """
        Game session is full as soon as all players have joined the game.

        Returns:
        bool: True, if session is full
        """
        return self._n_players == self._next_id

    def get_id(self, player_name):
        """
        Return player ID and password by name.

        This function returns the ID and password that were assigned to the
        player.

        Parameters:
        player_name (str): name of a player that has already joined the game

        Returns:
        tuple(int, str, str):
            int: player ID, None if no such player exists
            str: password, None if no such player exists
            str: error message, if a problem occurred, None otherwise
        """
        if not player_name in self._player_ids:
            return None, None, 'no such player'

        player_id = self._player_ids[player_name]

        return player_id, self._passwords[player_id], None

    def game_over(self):
        """
        Retrieve the game status from the game instance.

        Returns:
        bool: True, if game has ended, else False
        """
        return self._game.game_over()

    def current_player(self):
        """
        Retrieve current player(s) from the game instance.

        Returns:
        list: player IDs
        """
        return self._game.current_player()

    def last_access(self):
        """
        Return time of last access.
        """
        return self._last_access

    def _update_last_access(self):
        """
        Update time of last access.
        """
        self._last_access = time.time()

    def game_move(self, move, player_id):
        """
        Pass player's move to the game instance.

        When this function is called, an event is triggered to wake up other
        threads waiting for the game state to change.

        Parameters:
        move (dict): the player's move
        player_id (int): ID of the player submitting the move

        Returns:
        str: error message in case the move was illegal, None otherwise (see AbstractGame.move)
        """
        with self._lock:
            ret = self._game.move(move, player_id)
            self._update_last_access()
            self.wake_up_threads()
            if player_id not in self._no_delay:
                self._no_delay.append(player_id)
            return ret

    def game_state(self, player_id, observer):
        """
        Retrieve the game state from the game instance.

        In addition to the information returned from the game instance, the IDs
        of the current players and the game status are added to the returned
        state.

        This function will block until the game state changes. Only then will
        the updated state be sent back to the client. This is more efficient
        than polling. To avoid deadlocks, the function never blocks in certain
        situations:

        - when the game has just started and no move has been performed yet
        - when it is the client's turn to submit a move
        - when the client just performed a move and wants to get the new state
        - when the game has ended and moves are no longer possible
        - when the game was restarted and a client still has to get the old game's state

        To achieve this, the thread that changes the state triggers an event to
        wake up other threads waiting for that event.

        If the game has been restarted by some client, then for a single time
        the state of the previous game is returned to each client. This is
        necessary for a client to be able to detect the end of the previous
        game. See function restart_game for details.

        A list containing IDs is used for deciding whether the state should be
        returned immediately or only after it changes. At the same time, the
        function has to distinguish between active players and passive
        observers. Since observers are assigned the same IDs as the observed
        clients, the IDs have to be converted internally. The observer's IDs are
        increased so they come after the regular IDs: 0...n-1 = players,
        n...2n-1 = observers.

        Parameters:
        player_id (int): player ID
        observer (bool): if True, client requesting the state is a passive observer

        Returns:
        dict: game state
        """
        p_id = player_id
        if observer:
            p_id += self._n_players # convert observer IDs

        # wait for game state to change:
        if (not self._game.game_over()
            and not p_id in self._game.current_player()
            and not p_id in self._in_previous_game
            and not p_id in self._no_delay):
            self._state_change.clear()
            self._state_change.wait()

        # if required, return the previous game's state:
        # (this must NOT be done inside the lock below to avoid deadlocks)
        if p_id in self._in_previous_game:
            self._in_previous_game.remove(p_id)
            return self._assemble_state(self._previous_game, player_id)

        # return current game's state:
        with self._lock:
            self._update_last_access()
            if p_id in self._no_delay:
                self._no_delay.remove(p_id)
            return self._assemble_state(self._game, player_id)

    def _assemble_state(self, game, player_id):
        """
        Prepare the state to be returned to the client by adding current
        player(s) and game status.

        Parameters:
        game (AbstractGame): game instance
        player_id (int): player ID

        Returns:
        dict: game state
        """
        state = game.state(player_id)
        state['current'] = game.current_player()
        state['gameover'] = game.game_over()
        return state

    def _new_game(self):
        """
        Instantiate a new game and add IDs to the no-delay list so that all
        clients can retrieve the state even before any move has been performed.
        The observer's IDs are appended to the regular IDs. See function
        game_state for details.
        """
        self._game = self._game_class(self._n_players)
        self._no_delay = list(range(self._n_players * 2))

    def restart_game(self):
        """
        Restart the game.

        The game instance is replaced with a new one. The old instance is
        stored. This is necessary to allow the other clients to detect the end
        of the previous game. Otherwise, they would suddenly find themselves in
        a new game without being notified about it. To achieve this, a list of
        client IDs is created upon restarting a game. When a client then calls
        the state function, the state of the previous game is returned a single
        time, and the client's ID is removed from the list. From then on, the
        client will receive the game state of the new game instance.

        Only the client who started the game can restart it.
        """
        # store old game instance and a list of player IDs:
        if self._game.game_over():
            self._in_previous_game = list(range(1, self._n_players * 2))
            self._previous_game = copy.deepcopy(self._game)

        # create new game instance:
        self._new_game()

        # wake up other threads waiting for the game state to change:
        self.wake_up_threads()

    def _password(self, length=5):
        """
        Generate a unique password.

        Parameters:
        length (int): length of the password (optional)

        Returns:
        str: the password
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def password_valid(self, player_id, password):
        """
        Check if password and player ID match.

        Parameters:
        player_id (int): player ID
        password (str): password

        Returns:
        bool: True, if password valid
        """
        return player_id in self._passwords and self._passwords[player_id] == password

    def wake_up_threads(self):
        """
        Wake up other threads waiting for the game state to change.
        """
        self._state_change.set()

    def mark_timed_out(self):
        """
        Mark game session as timed out.
        """
        self._timed_out = True

    def timed_out(self):
        """
        Check if game session has timed out.

        Returns:
        bool: True, if game session has timed out
        """
        return self._timed_out
