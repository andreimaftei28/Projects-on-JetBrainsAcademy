from django.contrib import admin

# Register your models here.

from .models import Video, Tag, VideoTag

admin.site.register(Video)
admin.site.register(VideoTag)
admin.site.register(Tag)