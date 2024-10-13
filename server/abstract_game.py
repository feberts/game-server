"""
This module provides a base class for games.
"""

class AbstractGame:
    """
    Base class for games.

    This class serves as an abstract base class for games. Every new game must be derived from this class and implement all its methods. These methods will be called by the framework. Furthermore, every new game must be added to the list of available games. See the documentation for details on how to add new games.
    
    None of the methods may raise exceptions. Instead, flags and error messages must be returned to respond to invalid arguments. The flags and messages are then send back to the client where they are returned from an API function. So make sure to return meaningful messages.
    
    In some cases the framework performes checks before it calls a method. In such a case you can assume, that the argument passed is valid. See the methods descriptions for which parameters this may apply.
    """

    def state(self, player_id):
        """
        Returns the game state.

        This can be the complete state of the game or just specific information for a specific player. What information is returned depends entirely on the game. In some games all information is available to all players, in other games players can possess information that is hidden from the others.

        Parameters:
        player_id (int): player id (no parameter check needed)

        Returns:
        dict: game state
        """
        raise NotImplementedError

#TODO hier weiter

    def move(self, move):
        """
        To submit a move.

        A players move is passed as a dictionary. The content of this dictionary entirely depends on the game. Hence

        Parameters:
        move (dict): a players move

        Returns:
        tuple(bool, str): Summe von a und b

        Raises:
        TypeError: falls Summenbildung wegen falschen Typs nicht moeglich
        """
        raise NotImplementedError
        # return <move valid/illegal and error message>

# TODO
# - min number of player
# - max number of players
