from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import VacancyForm, ResumeForm
from resume.models import Resume
from vacancy.models import Vacancy
# Create your views here.
class MainPageView(View):

    def get(self,request, *args, **kwargs):

        return render(request, "authentification/menu.html")

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "authentification/home.html")

class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = "login"
    template_name = "authentification/signup.html"

class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = "authentification/login.html"


class NewResumeView(View):

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)

        if form.is_valid():
            clean_data = form.cleaned_data
            description = clean_data["description"]
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    new_res = Resume(description=description, author=request.user)
                    new_res.save()
                    del new_res
                    return redirect("/home")
                else:
                    return HttpResponseForbidden()
            else:
                return redirect("/home")

        return HttpResponseForbidden()


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)

        if form.is_valid():
            clean_data = form.cleaned_data
            description = clean_data["description"]
            if request.user.is_authenticated:
                if request.user.is_staff:
                    new_vac = Vacancy(description=description, author=request.user)
                    new_vac.save()
                    del new_vac
                    return redirect("/home")
                else:
                    return HttpResponseForbidden()
            else:
                return redirect("/home")
        return HttpResponseForbidden()
