# Game server

This project provides a server for multiplayer games. The main features are:

- a framework that allows new games to be added easily
- a uniform yet flexible API for all games

Possible areas of application include:

- programming courses in which students implement game clients
- projects in the area of reinforcement learning
- multiplayer game development in general

## Quickstart

To try this project on your machine, start the server by running `server/game_server.py`. Then run two tic-tac-toe clients (`client/tictactoe_client.py`) in separate shells. No further configuration is required.

## Operating the server

Server and API are implemented in plain Python. TCP sockets are used for communication. There are no external dependencies.

Configuration:

To run the server in a network, edit IP and port in the configuration file (`server/config.py`). Other than that, the log level for server and framework can be set there, as well as a timeout for inactive game sessions.

## Adding new games

Adding a new game is quite easy:

1. Add a new module to `server/`.
2. In this module, implement a class that is derived from `abstract_game.AbstractGame`.
3. Override all the base class's methods.
4. Add the new class to the list of games (`server/games.py`).
5. Write a documentation for the new game.

Notes:

- The documentation of the game base class (`AbstractGame`) should give you a good idea of how the framework operates. Use that as a guide, while implementing your game.
- It is not necessary to add any code to the API. It was designed to be compatible with any game. What you can do, optionally, is to implement an API wrapper for your game. Use the tic-tac-toe API wrapper as an example.

## API documentation

Documentation of class `GameServerAPI`.

This module provides an API for communicating with the game server. The API can be used to

- start a game that other clients can join
- join a game that was started by another client
- submit moves to the server
- request the game state
- passively observe other players
- reset a game without starting a new session

```
start_game(server, port, game, token, players, name='')
    Start a game.

    This function asks the server to start a game. Other clients can use the
    join function to join that game. To be able to join, they need to know the
    chosen token. The token is used to identify the game session. It can be any
    string. A repeated call of this function will end the previous session and
    start a new one, which other players can join.

    The game starts as soon as the specified number of clients has joined the
    game. The function then returns the player ID. The server assigns IDs in the
    range 0...players-1 to all players that join the game.

    The optional name parameter makes it possible for other clients to passively
    observe your playing by joining a game using the watch function. They will
    be able to retrieve the same game state from the server as you.

    Parameters:
    server (str): server
    port (int): port number
    game (str): name of the game
    token (str): name of the game session
    players (int): total number of players
    name (str): player name (optional)

    Returns:
    tuple(int, str):
        int: player ID, if the game was successfully started, else None
        str: error message, if a problem occurred, None otherwise

    Raises:
    AssertionError: for invalid arguments

join_game(server, port, game, token, name='')
    Join a game.

    This function lets a client join a game that another client has started by
    calling the start function. To be able to join, the correct token must be
    provided. The token is used to identify a specific game session.

    The game starts as soon as all clients have joined the game. The function
    then returns the player ID. The server assigns IDs in the range
    0...players-1 to all players that join the game.

    The optional name parameter makes it possible for other clients to passively
    observe your playing by joining a game using the watch function. They will
    be able to retrieve the same game state from the server as you.

    Parameters:
    server (str): server
    port (int): port number
    game (str): name of the game
    token (str): name of the game session
    name (str): player name (optional)

    Returns:
    tuple(int, str):
        int: player ID, if the game could be joined, else None
        str: error message, if a problem occurred, None otherwise

    Raises:
    AssertionError: for invalid arguments

move(**kwargs)
    Submit a move.

    This function is used to submit a move to the game server. The move must be
    passed as keyword arguments. Refer to the documentation of a specific game
    to find out about the required or available arguments. If it is not your
    turn to submit a move or if the move is invalid, the server replies with an
    error message.

    Parameters:
    kwargs (dict): player move as keyword arguments

    Returns:
    str: error message, if a problem occurred, None otherwise

state(blocking=True)
    Request the state.

    This function requests the game state from the server. The state is returned
    as a dictionary. Refer to the documentation of a specific game to find out
    about the structure and content of the dictionary.

    This function will block until the game state changes. Only then the server
    will respond with the updated state. This is more efficient than polling.
    The function can also be used in a non-blocking way. Furthermore, the
    function does not block, if it is the client's turn to submit a move, or if
    the game has ended.

    Parameters:
    blocking (bool): use function in blocking mode (default)

    Returns:
    tuple(dict, str):
        dict: game state if state could be retrieved, else None
        str: error message, if a problem occurred, None otherwise

watch(server, port, game, token, name)
    Observe another player.

    This function lets one client observe another client. By providing the name
    of the player to be observed, you will receive the same data calling the
    state function as that player does. Moreover, this function will return the
    player ID of the observed player.

    This function can only be called, after the specified game session has
    already been started.

    Parameters:
    server (str): server
    port (int): port number
    game (str): name of the game
    token (str): name of the game session
    name (str): name of player to observe

    Returns:
    tuple(int, str):
        int: ID of observed player, None in case of an error
        str: error message, if a problem occurred, None otherwise

    Raises:
    AssertionError: for invalid arguments

reset_game(self)
    Reset a game.

    This function resets the current game. There is no need to rejoin the game,
    and all players will keep their IDs. This is useful when simulating many
    games to collect data for AI training. Only the client who started the game
    can reset it.

    Returns:
    str: error message, if game could not be reset, None otherwise
```
