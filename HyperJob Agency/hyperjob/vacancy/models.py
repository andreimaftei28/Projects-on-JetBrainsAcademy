from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Vacancy(models.Model):
    description = models.TextField(max_length=1024)
    author = models.ForeignKey(User, related_name="job_author", on_delete=models.CASCADE)
