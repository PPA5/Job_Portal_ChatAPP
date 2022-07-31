from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ChatRoom


def index_view(request):
    return render(request, 'chatapp/custom_index.html', {
        'rooms': ChatRoom.objects.all(), 'users': User.objects.all()
    })


def room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chatapp/custom_room.html', {
        'room': chat_room,
    })

def user_view(request, user_name):
    user_chat = User.objects.get(username=user_name)
    return render(request, 'chatapp/custom_user.html', {
        'user': user_chat,
    })