from django import forms
from .models import ForumThread, ThreadComment

# TODO: Translate labels

class ThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title']


class ThreadCommentForm(forms.ModelForm):
    class Meta:
        model = ThreadComment
        fields = ['content']
