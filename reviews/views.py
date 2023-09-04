from django.shortcuts import render
from django.views.generic import TemplateView

from reviews.models import Review


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.values()

        context = {}

        if len(reviews) > 0:
            context["reviews"] = reviews

        return render(request=request, template_name=self.template_name, context=context)