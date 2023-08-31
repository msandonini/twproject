from django import views
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from mediapop.models import Media


# Create your views here.


class IndexView(TemplateView):
    template_name = "mediapop/index.html"


class MediaView(TemplateView):
    template_name = "mediapop/media.html"

    def get(self, request, *args, **kwargs):
        media = Media.objects.values()

        print("[MEDIA] ", media)

        context = {}

        if len(media) > 0:
            context["media"] = media

        return render(request=request, template_name=self.template_name, context=context)
