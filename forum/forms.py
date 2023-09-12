from django import forms
from .models import ForumThread, ThreadComment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title']
        labels = {
            'title': 'Titolo'
        }


class ThreadCommentForm(forms.ModelForm):
    class Meta:
        model = ThreadComment
        fields = ['content']

        labels = {
            'content': ''
        }
