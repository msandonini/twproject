from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView

from mediapop.models import Media, MediaVote
from reviews.models import Review


# Create your views here.


class IndexView(TemplateView):
    template_name = "mediapop/index.html"


class MediaView(TemplateView):
    template_name = "mediapop/media-index.html"

    def get(self, request, *args, **kwargs):
        items_per_page = 15

        q_name = request.GET.get('name')
        q_media_type = request.GET.get('type')
        q_order_by = request.GET.get('order_by')

        media = Media.objects.annotate(users_vote=Avg('mediavote__vote'))
        media = media.annotate(reviewers_vote=Avg('review__vote'))

        if q_name:
            media = media.filter(name__contains=q_name)

        if q_media_type:
            media = media.filter(media_type=q_media_type)

        if not q_order_by:
            q_order_by = "name"
        media = media.order_by(q_order_by)

        paginator = Paginator(media, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "media": page
        }

        return render(request=request, template_name=self.template_name, context=context)


class MediaDetailView(DetailView):
    model = Media
    template_name = 'mediapop/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["users_vote"] = MediaVote.objects.filter(media=context.get("object")).aggregate(Avg('vote'))['vote__avg']
        context["reviewers_vote"] = Review.objects.filter(media=context.get("object")).aggregate(Avg('vote'))['vote__avg']

        print(context)

        return context

    # TODO: Write POST to accept user votes


class UserLoginView(FormView):
    template_name = "mediapop/login-form.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        # You can customize the success message as needed
        return HttpResponse("")


class UserSignupView(FormView):
    template_name = "mediapop/signup-form.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='User')
        user.groups.add(group)

        auth.login(self.request, user)
        # Redirect to a success page or do something else
        return HttpResponse("")
