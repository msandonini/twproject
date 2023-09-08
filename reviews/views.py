from functools import wraps

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
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()

        context = {}

        if len(reviews) > 0:
            context["reviews"] = reviews

        return render(request=request, template_name=self.template_name, context=context)


@method_decorator(reviewer_required, name='dispatch')
class CreateReviewView(FormView):
    form_class = ReviewForm
    template_name = 'review-form.html'

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
    template_name = "review-detail.html"

    def get_context_data(self, **kwargs):
        context = {}

        review_pk = self.kwargs['pk']
        review = Review.objects.get(pk=review_pk)

        context["review"] = review

        return context
