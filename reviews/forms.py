from django import forms

from reviews.models import Review, ReviewComment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'cover', 'vote', 'text']
        labels = {
            'title': 'Titolo',
            'cover': 'Copertina',
            'vote': 'Voto',
            'text': 'Testo'
        }


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ["text"]
        labels = {
            'text': ''
        }
