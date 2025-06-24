from django.db import models
from django.conf import settings
from users.models import CustomUser
class Category(models.Model):
    name = models.CharField(max_length=100)
    Category_img = models.ImageField(upload_to='Category_img/', blank=True, null=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Stream(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True , default='game')
    status = models.CharField(max_length=20, choices=[('live', 'مباشر'), ('upcoming', 'قادم'), ('ended', 'انتهى')], default='live')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title