from django.urls import re_path

from . import consumers

websocket_urlpatterns = [

    #the \w+ means that anything after the chat is going to be picked up
    #room_name is the variable
    # $ prevents more data from being captured
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]