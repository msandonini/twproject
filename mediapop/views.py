from django import views
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from mediapop.models import Media


# Create your views here.


class IndexView(TemplateView):
    template_name = "mediapop/index.html"


class MediaView(TemplateView):
    template_name = "mediapop/media.html"

    def get(self, request, *args, **kwargs):
        media = Media.objects.values()

        context = {}

        if len(media) > 0:
            context["media"] = media

        return render(request=request, template_name=self.template_name, context=context)


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
