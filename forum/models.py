from django.contrib.auth.models import User
from django.db import models

from mediapop.models import Media


# Create your models here.


class ForumThread(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forum thread '{self.title}' about {self.media.name}"


class ThreadComment(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by @{self.user.username} in thread '{self.thread.title}'"
