from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, Http404
from django.conf import settings
import json
from datetime import datetime, date


# Create your views here.
def get_news():
    with open(settings.NEWS_JSON_PATH, "r") as f:
        return json.load(f)


class UnderConstructionPageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")


class NewsIndexPageView(View):
    def get(self, request, *args, **kwargs):
        news = get_news()
        news_sorted = dict()
        for n in news:
            created_date = datetime.strptime(n["created"], "%Y-%m-%d %H:%M:%S").date()
            news_sorted[created_date] = news_sorted.get(created_date, list()) + [n]
        news_sorted = {k.strftime("%Y-%m-%d"): v for k, v in sorted(news_sorted.items(), reverse=True)}

        return render(request, "news/index.html", {"news": news_sorted})


class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = get_news()
        context = list(filter(lambda x: x['link'] == kwargs['news_id'], news))[0]
        if context:
            return render(request, "news/news_detail.html", context=context)
        else:
            raise Http404(f"News #{kwargs['news_id']} not found")
