import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from base.models import User
from django.shortcuts import redirect
from chat.models import ChatMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"private_chat_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        reciepient = text_data_json["reciepient"]
        sender = self.user

        reciepient = await self.get_user(reciepient)

        await self.save_chat_message(sender, reciepient, message)

        # Send message to reciepient
        await self.channel_layer.group_send(
            f"private_chat_{reciepient}",
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )

    @database_sync_to_async
    def save_chat_message(self, sender, reciepient, message):
        ChatMessage.objects.create(
            sender=sender,
            reciepient=reciepient,
            body=message
        )

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
