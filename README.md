# Multiplayer game server

This project provides a lightweight server for turn-based multiplayer games.

### Main features

- multiple parallel game sessions
- a framework that allows new games to be added easily
- a uniform yet flexible API for all games
- an observer mode to watch another client play

### Possible areas of application

- development of turn-based multiplayer games in general
- programming courses in which students implement game clients
- implementing separate clients for input and output using the observer mode
- small projects in the area of reinforcement learning

## Quick start

To try this project on your machine, start the server (`server/game_server.py`). Then run two clients (`client/tictactoe_client.py`) in separate shells. No further configuration is required.

## Operating the server

Server and API are implemented in plain Python. TCP sockets are used for communication. There are no external dependencies.

To run the server in a network, edit IP and port in the configuration file (`server/config.py`). Other than that, the log level for server and framework can be set there, a timeout for inactive game sessions, as well as parameters for TCP connections.

## API documentation

Module `game_server_api` provides an API for communicating with the game server. The API can be used to

- start a game that other clients can join
- join a game that was started by another client
- submit moves to the server
- request the game state
- passively observe another player
- reset a game without starting a new session

The module is well documented. This should be sufficient to become familiar with the API.

## Adding new games

Adding a new game is quite easy:

1. Add a new module to directory `server/`.
2. In this module, implement a class that is derived from `abstract_game.AbstractGame`.
3. Override all the base class's methods.
4. Add the new class to the list of games (`server/games_list.py`).
5. Write an API documentation for the new game.

Notes:

- The documentation of the game base class (file `abstract_game.py`) should give you a good idea of how the framework operates. Use that as a guide, while implementing your game.
- It is not necessary to add any code to the API module. It was designed to be compatible with any game. What you can do, optionally, is to implement an API wrapper for your game. Use the tic-tac-toe API wrapper as an example.
- The API documentation should include information on the arguments expected by the function for submitting moves. The structure and content of the dictionary as returned by the function for retrieving the game state should also be explained.
