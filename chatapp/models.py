from django.contrib.auth.models import User
from django.db import models
import time

class ChatRoom(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class ChatMessage(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'

class UserChatMessage(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='from_user')
    target = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='to_user')
    content = models.CharField(max_length=512)
    timestamp = models.FloatField(default = time.time(), null= False)
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.target.username}: {self.content} [{self.timestamp}]'