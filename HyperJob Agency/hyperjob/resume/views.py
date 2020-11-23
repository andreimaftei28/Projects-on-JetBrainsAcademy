from django.shortcuts import render
from .models import Resume
# Create your views here.
def resume_view(request):
    resumes = Resume.objects.all()
    context = {
        "resumes": resumes
    }
    return render(request, "resume/resumees.html", context)