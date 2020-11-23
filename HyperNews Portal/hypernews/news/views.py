from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
import json, itertools
import datetime

def get_json_obj():
    with open(settings.NEWS_JSON_PATH, "r") as file:
        json_obj = json.load(file)
    return json_obj

def create(request, *args, **kwargs):
    if request.method == "POST":
        news_obj = get_json_obj()
        last_link = max(item["link"] for item in news_obj)


        with open(settings.NEWS_JSON_PATH, "w") as news_file:

            news_item = {
                "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "text": request.POST.get("text"),
                "title": request.POST.get("title"),
                "link": last_link + 1,
                "image": ""
            }
            news_obj.append(news_item)
            json.dump(news_obj, news_file)
        return redirect("/news/")
    else:
        return render(request, "create_news.html" )




class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")

class FirstPageView(View):
    def get(self, request, link=0, *args, **kwargs):

        json_obj = get_json_obj()
        json_news = {}
        for item in json_obj:
            date = item["created"].split()
            q = request.GET.get("q")
            if q:
                if q in "".join(item["title"].lower().split()):
                    json_news.setdefault(date[0], []).append(item)
            else:
                json_news.setdefault(date[0], []).append(item)
            if item["link"] == link:
                return render(request, "news.html", item)
        context = {
            "news": {
                k: json_news[k] for k in sorted(json_news, reverse=True)
            }
        }
        return render(request, "main.html", context)



class NewsView(View):

    def get(self, request, link, *args, **kwargs):

        json_obj = get_json_obj()

        data = {}
        for d in json_obj:
            if d['link'] == link:
                data['title'] = d['title']
                data['created'] = d['created']
                data['text'] = d['text']
                if "image" not in d:
                    d["image"] = ""
                    data["image"] = d["image"]
                else:
                    data["image"] = d["image"]
                break
        return render(request, 'news.html',
                      context={'title': data['title'],
                               'created': data['created'],
                               'text': data['text'],
                               "image": data["image"]
                            })