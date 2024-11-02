"""
Game base class.

This module provides a base class for games.
"""

class AbstractGame:
    """
    Base class for games.

    This class serves as a base class for games. Every new game must be derived from this class and implement all its methods. These methods will be called by the framework. Furthermore, every new game must be added to the list of available games. See the documentation for details on how to add new games.

    In some cases, the framework performs checks before it calls a method. In such a case, it can be assumed, that the argument passed is valid. Refer to the method descriptions to see which parameters this may apply to.

    None of the methods may raise exceptions. If this happens anyway, the framework will catch the exception to prevent the server from crashing, log this event and report a generic error message back to the client, but it will also stop the execution of that game.
    TODO delete game instance if an exception was raised by that game instance
    """

    def __init__(self, players):
        """
        Constructor.

        The framework assigns IDs in the range 0..players-1 to all players that join a game. It then passes the total number of players to the constructor. The framework makes sure, that only a defined number of players can join the game. The range of the number of allowed players is specified by functions min_players and max_players. The desired number of players is provided by the client starting a new game.

        Parameters:
        players (int): number of players (no parameter check required)
        """
        raise NotImplementedError

    def min_players(): # no self parameter
        """
        Returns the minimal number of players.

        This function reports the minimal number of players required to play the game to the framework.

        Returns:
        int: minimal number of players
        """
        raise NotImplementedError

    def max_players(): # no self parameter
        """
        Returns the maximal number of players.

        This function reports the highest allowed number of players in the game to the framework.

        Returns:
        int: highest allowed number of players
        """
        raise NotImplementedError

    def current_player(self):
        """
        Returns the current player's ID.

        A game class must keep track of which player must perform the next move. This function reports this player's ID to the framework. In return, the framework makes sure, that no other than the current player can submit a move.

        Returns:
        int: current player's ID
        """
        raise NotImplementedError

    def move(self, args):
        """
        Submit a move.

        A player's move is passed as a dictionary. The content of this dictionary entirely depends on the needs of the game. The API function to submit a move on the client side accepts the data as keyword arguments. Those keyword arguments are then converted to a dictionary. It is important to let the user of the API know about the names of these keywords and the expected data types of their values. See the documentation on how to add new games for more details.

        The framework makes sure, that only the current player can submit a move. The framework also guaranties, that the argument is of type dictionary, but the validity of the contained data must be checked thoroughly by the implementer of the game class.

        In order to respond to invalid moves, error messages must be returned. These are then sent back to the client, where they are returned from an API function. So make sure to return meaningful messages. If a move is valid, None must be returned.

        Parameters:
        args (dict): the current player's move (must be checked)

        Returns:
        str: error message in case the move was illegal, None otherwise
        """
        raise NotImplementedError

    def game_over(self):
        """
        Returns the game status.

        A boolean value is returned indicating whether the game has ended or is still active. After the game has ended, the framework makes sure that moves can no longer be submitted.

        Returns:
        bool: True, if game has ended, else False
        """
        raise NotImplementedError

    def state(self, player_id):
        """
        Returns the game state as a dictionary.

        This can be the complete state of the game, or just specific information for a specific player. What information is returned depends entirely on the game. In some games all information is available to all players, in other games players can possess information that is hidden from the others.

        It is important to let the user of the API know how the dictionary is structured, so its content can be accessed properly. See the documentation on how to add new games for more details.

        The framework will add additional data to the state after it is returned by this function. The following information is added:

        - the current player's ID as returned by function current_player; the framework will add it automatically as the value to a key named 'current'; this way, all players are aware of who's turn it is
        - a boolean value as returned by function game_over indicating whether the game has ended or is still active; the framework will add it automatically as the value to a key named 'gameover'

        Parameters:
        player_id (int): ID of the player requesting the state (no parameter check required)

        Returns:
        dict: game state
        """
        raise NotImplementedError
