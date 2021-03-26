from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, Http404
from django.conf import settings
import json
from datetime import datetime, date
import random


# Create your views here.
def get_news():
    with open(settings.NEWS_JSON_PATH, "r") as f:
        return json.load(f)


def save_news(news):
    with open(settings.NEWS_JSON_PATH, "w") as f:
        return json.dump(news, f)


def get_new_link(news):
    links = {a['link'] for a in news}
    while True:
        link = random.randint(1, 10000)
        if link not in links:
            return link


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


class CreateNews(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/news_create.html")

    def post(self, request, *args, **kwargs):
        news = get_news()
        new = {'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               'text': request.POST.get("text"),
               'title': request.POST.get("title"),
               'link': get_new_link(news)
               }
        news.append(new)
        save_news(news)
        return redirect("news_index")
