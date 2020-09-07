from channels.routing import include
from channels.routing import route
from otree.channels.routing import channel_routing

from game.consumers import ws_connect as game_ws_connect,\
    ws_message as game_ws_message,    \
    ws_disconnect as game_ws_disconnect


#################################################
#  Sockets for xp application
game_routing = [route("websocket.connect", game_ws_connect),
                route("websocket.receive", game_ws_message),
                route("websocket.disconnect", game_ws_disconnect), ]

##################################################################################################
##################################################################################################
channel_routing += [
    include(game_routing, path=r"^/game/activity"),
]
