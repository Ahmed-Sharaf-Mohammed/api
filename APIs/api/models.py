from django.db import models

# models.py
from django.db import models

class Upload(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True)
    filename = models.CharField(max_length=255)
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.filename
