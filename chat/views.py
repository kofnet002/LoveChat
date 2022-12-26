
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from chat.models import ChatMessage
from base.models import User
# from authy.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator


@login_required(login_url='login')
def inbox(request):
    user = request.user
    messages = ChatMessage.get_message(user=request.user)
    active_direct = None
    directs = None
    # profile = get_object_or_404(User, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = ChatMessage.objects.filter(
            user=user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'chat_messages': messages,
        'active_direct': active_direct,
        # 'profile': profile,
    }
    return render(request, 'chat/direct.html', context)


@login_required(login_url='login')
def get_chat(request, username):
    user = request.user
    messages = ChatMessage.get_message(user=user)
    active_direct = username
    directs = ChatMessage.objects.filter(
        user=user, reciepient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'chat_messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'chat/inbox.html', context)


@login_required(login_url='login')
def send_message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        ChatMessage.sender_message(from_user, to_user, body)
        return redirect('message')


# def UserSearch(request):
#     query = request.GET.get('q')
#     context = {}
#     if query:
#         users = User.objects.filter(Q(username__icontains=query))

#         # Paginator
#         paginator = Paginator(users, 8)
#         page_number = request.GET.get('page')
#         users_paginator = paginator.get_page(page_number)

#         context = {
#             'users': users_paginator,
#         }

#     return render(request, 'directs/search.html', context)


# def NewConversation(request, username):
#     from_user = request.user
#     body = ''
#     try:
#         to_user = User.objects.get(username=username)
#     except Exception as e:
#         return redirect('search-users')
#     if from_user != to_user:
#         Message.sender_message(from_user, to_user, body)
#     return redirect('message')
