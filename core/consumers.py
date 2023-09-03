# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

"""
    This is a synchronous WebSocket consumer that accepts all connections, 
    receives messages from its client, and echos those messages back to the 
    same client. For now it does not broadcast messages to other clients 
    in the same room.
"""


class ChatConsumer(WebsocketConsumer):
    """ WebSocket consumer for Chat"""

    def connect(self):
        """Accept the connection for WebSocket communication"""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        """Will execute when the connection is closed"""
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        """Receive the text data from the websocket and process it"""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message})

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))


