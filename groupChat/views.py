from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Message, Room, Topic, User
from .form import RoomForm
from django.db.models import Q

# Create your views here.


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages[:3],
    }
    return render(request, 'groupChat/group.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'groupChat/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            profileimg=request.FILES.get('profileimg'),
        )
        return redirect('group-chat')
    context = {'form': form, 'topics': topics}
    return render(request, 'groupChat/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowd here!!!')

    if request.method == 'POST':
        if request.FILES.get('profileimg') == None:
            topic_name = request.POST.get("topic")
            topic, create = Topic.objects.get_or_create(name=topic_name)
            room.name = request.POST.get('name')
            room.topic = topic
            room.description = request.POST.get('description')
            room.profileimg = room.profileimg

        if request.FILES.get('profileimg') != None:
            room.profileimg = request.FILES.get('profileimg')

            topic_name = request.POST.get("topic")
            topic, create = Topic.objects.get_or_create(name=topic_name)
            room.name = request.POST.get('name')
            room.topic = topic
            room.description = request.POST.get('description')
            room.profileimg = room.profileimg
            
        room.save()
        return redirect('group-chat')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'groupChat/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowd here!!!')

    if request.method == 'POST':
        room.delete()
        return redirect('group-chat')
    return render(request, 'groupChat/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowd here!!!')

    if request.method == 'POST':
        message.delete()
        return redirect('group-chat')
    return render(request, 'groupChat/delete.html', {'obj': message})


@login_required(login_url='login')
def topicsPage(request):
    topics = Topic.objects.all()

    context = {'topics': topics}
    return render(request, 'groupChat/topics.html', context)
