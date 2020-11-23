from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):

    description = models.TextField(max_length=1024)
    author = models.ForeignKey(User, related_name="resume_author", on_delete=models.CASCADE)

