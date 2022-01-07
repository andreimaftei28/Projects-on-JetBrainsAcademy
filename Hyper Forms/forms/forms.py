
from django import forms
from .models import Participant

class RegisterForm(forms.ModelForm):
    name = forms.CharField(label="your name")
    age = forms.IntegerField(label="your age")
    favorite_book = forms.CharField(label="Your favorite book")
    class Meta:
        model = Participant
        fields = [
            "name",
            "age",
            "favorite_book"
        ]