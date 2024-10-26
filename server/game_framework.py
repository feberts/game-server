"""
Game framework.

This module implements the game framework. The framework is responsible for managing active games. It serves as an intermediary between the server and active game instances.

Client requests are parsed and the appropriate actions are performed. The following list shows the types of requests the framework can handle and the resulting actions:

- start: instantiate game class objects
- join: assign clients to games
- move: forward player moves to game instances
- state: report the game state to clients

To perform these actions, the framework calls the corresponding methods of a game class, if necessary.
"""

import utility

class GameFramework:
    """
    Class GameFramework.
    
    This class manages active games and handles the interaction between clients and game instances.
    """
    def __init__(self):
        #TODO
        pass

    def handle_request(self, request):
        """
        Handling a client request.

        This function is called by the server. It identifies the type of the request and redirects it to the corresponding method. The returned data is handed back to the server and then sent to the client.

        Parameters:
        request (dict): client request

        Returns:
        dict: reply
        """
        if 'type' not in request:
            return utility.framework_error("key 'type' of type str missing")

        handlers = {'start_game':self.start_game}
        
        if request['type'] not in handlers:
            return utility.framework_error('invalid request type')
        
        return handlers[request['type']](request)

    def start_game(self, request):
        """
        TODO
        """
        return {'status':'ok', 'message':'starting game', 'data':{'player_id':13}}
        
        
