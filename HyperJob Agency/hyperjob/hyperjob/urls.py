"""hyperjob URL Configuration

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
from django.urls import path
from authentification.views import MainPageView, MySignupView, MyLoginView, \
    HomePageView, NewResumeView, NewVacancyView
from django.contrib.auth.views import LogoutView
from vacancy.views import vacancy_jobs_view
from resume.views import resume_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainPageView.as_view()),
    path("home/", HomePageView.as_view()),
    path("signup", MySignupView.as_view()),
    path("login", MyLoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("vacancies/", vacancy_jobs_view),
    path("resumes/", resume_view),
    path("resume/new", NewResumeView.as_view()),
    path("vacancy/new", NewVacancyView.as_view())
]
