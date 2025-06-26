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
    thumbnail = models.ImageField(upload_to='thumbnails-stream/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True , default='game')
    status = models.CharField(max_length=20, choices=[('live', 'مباشر'), ('upcoming', 'قادم'), ('ended', 'انتهى')], default='live')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    
class Playlist(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ({self.owner.username})"


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.video and not self.stream:
            raise ValidationError("You must attach either a video or a stream.")
        if self.video and self.stream:
            raise ValidationError("You cannot attach both a video and a stream.")

    def __str__(self):
        content = self.video.title if self.video else self.stream.title
        return f"{content} in {self.playlist.name}"
