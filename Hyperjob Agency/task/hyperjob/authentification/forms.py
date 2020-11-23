
from django import forms

from vacancy.models import Vacancy
from resume.models import Resume

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            "description"
        ]

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            "description"
        ]

