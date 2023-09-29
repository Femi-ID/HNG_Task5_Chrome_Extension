from django.db import models

# Create your models here.


class ScreenRecorder(models.Model):
    title = models.CharField(max_length=150)
    video_file = models.FileField(upload_to='videos/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-date_created', )

