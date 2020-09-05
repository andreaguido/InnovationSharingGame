from channels import Group as channelsGroup
from channels.sessions import channel_session
import random
import json
import channels
import logging
from .models import Player as OtreePlayer

from otree import constants_internal
import django.test
from otree.common_internal import (get_admin_secret_code)

client = django.test.Client()
ADMIN_SECRET_CODE = get_admin_secret_code()


#############################################
#############################################
# Connected to websocket.connect
def ws_connect(message):
    print("*********CONNECT_ACTIVITY************")
    channelsGroup("ACTIVITY_GROUP").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    print("*********RECEIVE_ACTIVITY************")
    # Decrypt the url: No info in the url in this app
    # Decrypt the received message
    jsonmessage = json.loads(message.content['text'])
    order = jsonmessage['order']
    # Get the data
    if order == "set_player_active":
        player_pk = jsonmessage['player_pk']
        myplayer = OtreePlayer.objects.get(pk=player_pk)
        myplayer.active = 1
        myplayer.save()
    elif order == "set_player_inactive":
        player_pk = jsonmessage['player_pk']
        myplayer = OtreePlayer.objects.get(pk=player_pk)
        myplayer.active = 0
        myplayer.save()
    ###############################
    # Example of a message from server to all clients connected to this channel "ACTIVITY_GROUP"
    # channelsGroup("ACTIVITY_GROUP").send({'text': json.dumps(
    #     {"order": "order_from_server"})}
    # )


###############################


# Connected to websocket.disconnect
def ws_disconnect(message):
    print("*********DISCONNECT_ACTIVITY************")
    channelsGroup("ACTIVITY_GROUP").discard(message.reply_channel)
