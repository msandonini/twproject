from django import forms

from reviews.models import Review, ReviewComment

# TODO: Translate labels

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'cover', 'vote', 'text']


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ["text"]
