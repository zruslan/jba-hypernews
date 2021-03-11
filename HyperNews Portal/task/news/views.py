from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404
from django.conf import settings
import json


# Create your views here.

class UnderConstructionPageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")


class SiteIndexPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/index.html")


class NewsView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as f:
            news = json.load(f)

        context = list(filter(lambda x: x['link'] == kwargs['news_id'], news))[0]
        if context:
            return render(request, "news/news_detail.html", context=context)
        else:
            raise Http404(f"News #{kwargs['news_id']} not found")
