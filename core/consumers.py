# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

"""
    The ChatConsumer that we have written is currently synchronous. 
    Synchronous consumers are convenient because they can call regular 
    synchronous I/O functions such as those that access Django models 
    without writing special code. However asynchronous consumers can 
    provide a higher level of performance since they don’t need to create 
    additional threads when handling requests.
"""


class ChatConsumer(AsyncWebsocketConsumer):
    """ WebSocket consumer for Chat"""

    async def connect(self):
        """Accept the connection for WebSocket communication"""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Will execute when the connection is closed"""

        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Receive the text data from the websocket and process it"""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message})

    async def chat_message(self, event):
        message = event["message"]

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


