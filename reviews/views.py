from functools import wraps

import bleach
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, CreateView

from mediapop.models import Media
from mediapop.views import get_recommendation_scores
from reviews.decorators import reviewer_required
from reviews.forms import ReviewForm
from reviews.models import Review


# Create your views here.

class IndexView(TemplateView):
    template_name = "reviews/index.html"

    def get_context_data(self, **kwargs):
        items_per_page = 4

        q_name = self.request.GET.get('name')
        q_media_type = self.request.GET.get('type')
        q_order_by = self.request.GET.get('order_by')
        q_recommended = (q_order_by == "recommended")

        media = None

        if not q_order_by or q_recommended:
            q_order_by = "-creation_time"

        if q_recommended and self.request.user.is_authenticated:
            # -- RECOMMENDATION SYSTEM --

            recommendation_scores = get_recommendation_scores(self.request)

            reviews = Review.objects.filter(media__media_type=recommendation_scores[0][0])

            reviews = reviews.order_by(q_order_by)
            if q_name:
                reviews = reviews.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

            if q_media_type:
                reviews = reviews.filter(media__media_type=q_media_type)

            for i in range(1, len(recommendation_scores)):
                tmp = Review.objects.filter(media__media_type=recommendation_scores[i][0])
                tmp = tmp.order_by(q_order_by)
                if q_name:
                    tmp = tmp.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

                if q_media_type:
                    tmp = tmp.filter(media__media_type=q_media_type)

                reviews = list(reviews) + list(tmp)
        else:
            reviews = Review.objects.all()

            if q_name:
                reviews = reviews.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

            if q_media_type:
                reviews = reviews.filter(media__media_type=q_media_type)

            reviews = reviews.order_by(q_order_by)

        paginator = Paginator(reviews, items_per_page)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "reviews": page
        }

        return context


@method_decorator(reviewer_required, name='dispatch')
class CreateReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review-form.html'

    def form_valid(self, form):
        media_pk = self.kwargs['pk']
        media = Media.objects.get(pk=media_pk)

        review = form.save(commit=False)
        review.media = media
        review.user = self.request.user

        review.save()

        review_pk = review.pk
        url = reverse("reviews:review_detail", args=[review_pk])

        return HttpResponseRedirect(url)


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
