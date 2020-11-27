from django.shortcuts import render, redirect
from.models import Tag, Video, VideoTag
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import VideoUploadForm
from hypertube.settings import MEDIA_ROOT as mr
from django.http import HttpResponse
# Create your views here.

class FirstPageView(View):

    def get(self, request, *args, **kwargs):

        return redirect("tube/")

class MainPageView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if request.GET.get("tag") is not None:
            tag = request.GET.get("tag")
            videos = Video.objects.filter(videotag__tag__name=tag)
            print(videos)
            context["tag"] = "#" + tag
        elif request.GET.get("q") is not None:
            q = request.GET.get("q")
            titles = list(Video.objects.values("title"))
            for tit in titles:
                if q in tit["title"]:
                    videos = Video.objects.filter(title=tit["title"])
        else:
            videos = Video.objects.all()
        context["videos"] = videos

        return render(request, "tube/main.html", context)


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = "http://127.0.0.1:8000/login/"
    template_name = "tube/signup.html"

class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = "tube/login.html"



def upload_video(request):

    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            item = data["video"]
            video = Video.objects.create(
                title=data["title"],
                file=item.name,
            )
            for tag in data["tags"].split():
                tg = Tag.objects.create(name=tag)
                VideoTag.objects.create(tag=tg, video=video).save()

            video.save()
            tg.save()
            with open(mr + item.name, "wb+") as file_storage:
                for chunk in item.chunks():
                    file_storage.write(chunk)
            return redirect("/tube/")


    else:
        form = VideoUploadForm()
        context = {
              "form": form
            }

    return render(request, "tube/upload.html", context)


def watch_video(request ,*args, **kwargs):
    video = Video.objects.get(id=kwargs["id"])

    context = {
        "video": video,
        "type": str(video.file).split(".")[-1],
        "tags": Tag.objects.filter(videotag__video=video)
    }
    return render(request, "tube/watch.html", context)

def video_handler(request, **kwargs):
    with open(mr.replace("/", "\\") + kwargs["video"][:-1] , "rb") as file:
        response = HttpResponse(file, content_type=f"video/{kwargs['video'][:-1].split('.')[-1]}")
        response["Accept-Ranges"] = "bytes"
    return response