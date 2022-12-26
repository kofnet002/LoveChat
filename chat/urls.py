from chat import views
from django.urls import path

urlpatterns = [
    path('message/inbox/', views.inbox, name="message"),
    path('message/inbox/<str:username>', views.get_chat, name="directs"),
    path('send/', views.send_message, name="send-directs"),
    # path('search/', views.UserSearch, name="search-users"),
    # path('new/<username>', views.NewConversation, name="conversation"),
]
