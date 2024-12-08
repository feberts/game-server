# Game server

This project provides a server for multiplayer games. The main features are:

- a framework that allows new games to be added easily
- a unified but flexible API for all games

Areas of application include

- programming courses in which students implement game clients
- projects in the area of machine learning
- competitive programming contests
- multiplayer game development in general

## Quick start

If you want to try this project on your machine, start the server by running `server/game_server.py`. Then run two tic-tac-toe clients (`client/tictactoe_client.py`) in separate shells. No further configuration is required.

## Operating the server

Server and API are implemented in plain Python. TCP sockets are used for communication. There are no external dependencies.

Configuration:

To run the server in a network, edit IP and port in the configuration file (`server/config.py`). Other than that, the log level for server and framework can be set there, as well as a timeout for inactive game sessions.

## Adding new games

Adding a new game is quite easy:

1. ...

## Using the API

- tabelle mit api-funktionen samt erläuterung
- anhand eines konkreten beispiels
