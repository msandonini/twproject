from django import views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
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


class LoginView(FormView):
    template_name = "mediapop/login-form.html"
    form_class = AuthenticationForm


class SignupView(FormView):
    form_class = UserCreationForm
