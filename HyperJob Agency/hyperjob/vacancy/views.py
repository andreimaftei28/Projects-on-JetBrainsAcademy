from django.shortcuts import render
from django.views import View
from .models import Vacancy



# Create your views here.


def vacancy_jobs_view(request):
    vacant_jobs = Vacancy.objects.all()
    context = {
        "vacancies": vacant_jobs
    }
    return render(request, "vacancy/vacantjobs.html", context)