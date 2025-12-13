# Multiplayer game server

A lightweight server and framework for turn-based multiplayer games.

### Features

- a framework that allows new games to be added easily
- a uniform yet flexible API for all games
- multiple parallel game sessions
- an observer mode to watch another client play

### Use cases

- development of turn-based multiplayer games such as board or card games
- programming courses in which students implement clients or new games
- implementing reinforcement learning agents

### Quick start

To try this project on your machine, start the server (`server/game_server.py`), then run two clients (`client/tictactoe_client.py`) in separate shells. No configuration is required.

### About this project

This server was developed for use in a university programming course, where students learn Python as their first programming language and have to work on projects in small groups.
Both the framework and the API are designed so that the programming skills acquired during the first term are sufficient to implement new games and clients. However, the use of the server is not limited to educational scenarios.

Due to the architecture of the framework and the design of the communication protocol, the server is not suited for real-time games.

## Operating the server

To run the server in a network, edit IP and port in the configuration file (`server/config.py`). The log level for server and framework can be specified there, as well as a timeout for inactive game sessions and parameters for TCP connections.

Server and API are implemented in plain Python. TCP sockets are used for communication. There are no external dependencies. This makes the server very easy to handle.

If you intend to run the server as a systemd service, you can use the provided unit file (`gameserver.service`) as a starting point.

## Implementing clients

Module `game_server_api` provides an API for communicating with the server. The API can be used to

- start a game session that other clients can join
- join a game session
- submit moves
- retrieve the game state
- passively observe another player
- restart a game without having to start a new session

You can take a look at the example clients to become familiar with the API. The API module itself is extensively documented.

## Adding new games

Adding a new game is quite easy. You simply derive from a base class and override its methods:

1. Create a new module in `server/games/`.
2. In this module, implement a class that is derived from `abstract_game.AbstractGame`.
3. Override all the base class's methods.
4. Add the new class to the list of games (`server/games_list.py`).

To make things even easier, you can use the template (`server/games/template.py`), which is structured like a tutorial.

No changes to the API are required when adding a new game. The API was designed to be compatible with any game. The function to submit a move accepts the data as keyword arguments (`**kwargs`). These are converted to a dictionary and sent to the server, where the dictionary is passed to the corresponding function of the game class. The game state is also sent back as a dictionary. This allows for a maximum of flexibility.

## Observer mode

A passive observer will receive the same data as the observed player does when retrieving the game state. This can be useful in a number of ways:

- The observer mode can be used to visualize the performance of a reinforcement learning agent.
- It can be used to split up the work in a team. One member could implement a client for the user interaction that verifies the input and sends it to the server. Another client could then be implemented to retrieve the state and render the game board.
- In a similar way, it can be used as a substitute for multithreading, which is usually not taught in a beginner programming course. Let's take a chat client as an example: Suppose you want to display incoming messages continuously while being able to write a new message at the same time. You could use two threads of execution to achieve this. Alternatively, the observer mode can be used to implement separate clients for input and output.

## Contributions

Code contributions are welcome. Feel free to open a pull request if you want to contribute a new game, a client, or new features to the server.
