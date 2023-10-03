from django.db import models


class VideoChunks(models.Model):
    session_id = models.CharField(max_length=200)
    chunk_number = models.PositiveIntegerField()
    total_chunks = models.PositiveIntegerField()
    video_chunk = models.FileField(upload_to='video_chunks/')

    def __str__(self):
        return self.session_id


class ScreenRecorder(models.Model):
    session_id = models.CharField(max_length=200)
    title = models.CharField(max_length=150)
    video_file = models.FileField(upload_to='videos/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-date_created', )

