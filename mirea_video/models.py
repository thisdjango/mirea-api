from django.db import models


# VideoData
class VideoData(models.Model):
    playlist_id = models.CharField(max_length=512)
    playlist_title = models.CharField(max_length=512)
    video_id = models.CharField(max_length=512)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=2048)
    image_url = models.CharField(max_length=1024)
