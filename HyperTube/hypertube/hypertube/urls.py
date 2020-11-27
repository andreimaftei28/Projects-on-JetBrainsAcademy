"""hypertube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from tube.views import MainPageView, FirstPageView, \
    MySignupView, MyLoginView, upload_video, watch_video, video_handler
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", FirstPageView.as_view()),
    path("tube/", MainPageView.as_view()),
    path("signup/", MySignupView.as_view()),
    path("login/", MyLoginView.as_view()),
    path("logout/",LogoutView.as_view()),
    path("tube/upload/", upload_video),
    re_path(r"watch/(?P<id>\w+)/", watch_video),
    re_path(r"(?P<video>\w+\.\w+/$)", video_handler)

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
