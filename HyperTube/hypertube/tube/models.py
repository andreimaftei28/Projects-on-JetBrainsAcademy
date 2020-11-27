from django.db import models

# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=255)

class Video(models.Model):

    file = models.FileField(upload_to="video/%y")
    title = models.CharField(max_length=255)


class VideoTag(models.Model):

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

