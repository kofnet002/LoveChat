from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/message/inbox/<str:username>', ChatConsumer.as_asgi()),
]
