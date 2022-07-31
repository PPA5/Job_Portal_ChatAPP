from email import message
import json
from msilib import text
from unicodedata import name

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chatapp.models import ChatRoom, ChatMessage, UserChatMessage
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q

class UserChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        #self.room_name = None
        #self.room_group_name = None
        #self.room = None
        self.to_user = None
        self.target = None
        self.user = None
        self.user_inbox = None  # new

    def connect(self):
        self.to_user = self.scope['url_route']['kwargs']['user_name'] 
        self.target = User.objects.get(username = self.to_user)
        self.user = self.scope['user']                                  
        self.user_inbox = f'inbox_{self.user.username}'  # new  
        self.room = ChatRoom.objects.get(name = 'online_users')
        self.accept()

        if self.user.is_authenticated:
            # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )

            self.send(json.dumps({
                'type': 'user_list',
                'users': [user.username for user in self.room.online.all()],
            }))
            self.room.online.add(self.user)
            
            to_message = UserChatMessage.objects.filter(Q(target= self.target) & Q(user = self.user))
            from_message = UserChatMessage.objects.filter(Q(target= self.user) & Q(user = self.target))
            user_message = to_message.union(from_message).order_by('timestamp')
            message = serializers.serialize("json", user_message)
            self.send(json.dumps({
                'type': 'history_msg',
                'message': message,
            }))
            
    def disconnect(self, close_code):
        if self.user.is_authenticated:
            # delete the user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            self.room.online.remove(self.user)
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']

        if type == 'oninput':
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{self.to_user}',
                {
                    'type': 'typing_message',
                    'user': self.user.username,
                    'message': message,
                }
            )
            return

        ts = text_data_json['timestamp']

        if type == 'delete_message':
            """
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{self.to_user}',
                {
                    'type': 'delete_message',
                    'timestamp': ts,
                }
            )
            """
            self.send(json.dumps({
                    'type': 'delete_message_delivered',
                    'timestamp': ts,
                }))
            UserChatMessage.objects.filter(Q(timestamp = ts) & Q(user = self.user) & Q(target = self.target)).update(deleted = True)
            return

        if type == 'updatemessage':
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{self.to_user}',
                {
                    'type': 'update_message',
                    'user': self.user.username,
                    'message': message,
                    'timestamp': ts,
                }
            )
            self.send(json.dumps({
                    'type': 'update_message_delivered',
                    'target': self.to_user,
                    'message': message,
                    'timestamp': ts,
                }))
            UserChatMessage.objects.filter(Q(timestamp = ts) & Q(user = self.user) & Q(target = self.target)).update(content = message, edited = True)
            return
        
        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
                f'inbox_{self.to_user}',
                {
                    'type': 'private_message',
                    'user': self.user.username,
                    'message': message,
                    'timestamp': ts,
                }
            )
        self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': self.to_user,
                'message': message,
                'timestamp': ts,
            }))
            
        target = User.objects.get(username = self.to_user)
        UserChatMessage.objects.create(user=self.user, target=target, content=message, timestamp = ts)

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def typing_message(self, event):
        self.send(text_data=json.dumps(event))
    
    def update_message(self, event):
        self.send(text_data=json.dumps(event))
    
    #def delete_message(self, event):
    #    self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))

    def user_list(self, event):
        self.send(text_data=json.dumps(event))
    # ---------------- end of new ----------------

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None  # new

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #defauld
        self.room_group_name = f'chat_{self.room_name}'                 #chat_default
        self.room = ChatRoom.objects.get(name=self.room_name)           #default
        self.user = self.scope['user']                                  #user1
        self.user_inbox = f'inbox_{self.user.username}'  # new          #inbox_user1

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,                                       #default
            self.channel_name,                                          #user1 channel name
        )

        # send the user list to the newly joined user
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        if self.user.is_authenticated:
            # -------------------- new --------------------
            # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # -------------------- new --------------------
            # delete the user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------
            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        # -------------------- new --------------------
        if message.startswith('/pm '):
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': self.user.username,
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            return
        # ---------------- end of new ----------------

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user.username,
                'message': message,
            }
        )
        ChatMessage.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    # -------------------- new --------------------
    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))