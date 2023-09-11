from functools import wraps

import bleach
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from mediapop.models import Media
from reviews.decorators import reviewer_required
from reviews.forms import ReviewForm
from reviews.models import Review


# Create your views here.

class IndexView(TemplateView):
    template_name = "reviews/index.html"

    def get_context_data(self, **kwargs):
        context = {
            "reviews": Review.objects.all()
        }

        return context


@method_decorator(reviewer_required, name='dispatch')
class CreateReviewView(FormView):
    form_class = ReviewForm
    template_name = 'reviews/review-form.html'

    def get_success_url(self):
        # TODO: Create redirect page for created review
        return reverse('review_detail', args=[self.kwargs['pk']])

    def form_valid(self, form):
        media_pk = self.kwargs['pk']
        media = Media.objects.get(pk=media_pk)

        review = form.save(commit=False)
        review.media = media
        review.user = self.request.user

        review.save()

        return HttpResponse("")


class ReviewDetailView(TemplateView):
    template_name = "reviews/review-detail.html"

    def get_context_data(self, **kwargs):
        context = {}

        review_pk = self.kwargs['pk']
        review = Review.objects.get(pk=review_pk)

        review_txt_vulnerable = review.text.replace("\n", "<br>")

        bleach_settings = {
            "tags": ["br"],
            "attributes": {}
        }

        context["review_text"] = bleach.clean(review_txt_vulnerable, **bleach_settings)

        context["review"] = review

        return context
