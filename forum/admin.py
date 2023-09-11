from django.contrib import admin

from forum.models import ForumThread, ThreadComment

# Register your models here.

admin.site.register(ForumThread)
admin.site.register(ThreadComment)
