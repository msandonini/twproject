from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, DeleteView

from forum.forms import ThreadForm, ThreadCommentForm
from forum.models import ForumThread, ThreadComment
from mediapop.models import Media
from mediapop.views import get_recommendation_scores
from reviews.models import ReviewComment


# Create your views here.

class IndexView(TemplateView):
    template_name = "forum/index.html"

    def get_context_data(self, **kwargs):
        items_per_page = 10

        q_name = self.request.GET.get('name')
        q_media_type = self.request.GET.get('type')
        q_order_by = self.request.GET.get('order_by')
        q_recommended = (q_order_by == "recommended")

        threads = None

        if not q_order_by or q_recommended:
            q_order_by = "-creation_time"

        if q_recommended and self.request.user.is_authenticated:
            # -- RECOMMENDATION SYSTEM --

            recommendation_scores = get_recommendation_scores(self.request)

            threads = ForumThread.objects.filter(media__media_type=recommendation_scores[0][0])

            threads = threads.order_by(q_order_by)
            if q_name:
                threads = threads.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

            if q_media_type:
                threads = threads.filter(media__media_type=q_media_type)

            for i in range(1, len(recommendation_scores)):
                tmp = ForumThread.objects.filter(media__media_type=recommendation_scores[i][0])
                tmp = tmp.order_by(q_order_by)
                if q_name:
                    tmp = tmp.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

                if q_media_type:
                    tmp = tmp.filter(media__media_type=q_media_type)

                threads = list(threads) + list(tmp)
        else:
            threads = ForumThread.objects.all()

            if q_name:
                threads = threads.filter(Q(title__contains=q_name) | Q(media__name__contains=q_name))

            if q_media_type:
                threads = threads.filter(media__media_type=q_media_type)

            threads = threads.order_by(q_order_by)

        paginator = Paginator(threads, items_per_page)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "threads": page
        }

        return context


class ThreadDetailView(TemplateView):
    template_name = 'forum/thread.html'

    def get_context_data(self, **kwargs):
        context = {}

        thread_pk = self.kwargs['pk']
        thread = ForumThread.objects.get(pk=thread_pk)

        context['thread'] = thread

        comments = ThreadComment.objects.filter(thread=thread_pk).order_by("-timestamp")
        context['comments'] = comments

        context['comment_form'] = ThreadCommentForm()

        return context

    def post(self, request, pk):
        thread = get_object_or_404(ForumThread, pk=pk)

        form = ThreadCommentForm(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user

            comment.save()

            return HttpResponse("")
        else:
            return HttpResponseBadRequest("Invalid form")


class CreateThreadView(CreateView):
    model = ForumThread
    form_class = ThreadForm
    template_name = 'forum/thread-form.html'

    def form_valid(self, form):
        media_pk = self.kwargs['pk']
        media = Media.objects.get(pk=media_pk)

        thread = form.save(commit=False)

        thread.media = media
        thread.author = self.request.user

        thread.save()

        thread_pk = thread.pk
        url = reverse('forum:thread', args=[thread_pk])

        return HttpResponseRedirect(url)
