from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, CreateView

from forum.forms import ThreadForm, ThreadCommentForm
from forum.models import ForumThread, ThreadComment
from mediapop.models import Media


# Create your views here.

class IndexView(TemplateView):
    template_name = "forum/index.html"

    def get_context_data(self, **kwargs):
        items_per_page = 10

        paginator = Paginator(ForumThread.objects.order_by("-creation_time"), items_per_page)
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
