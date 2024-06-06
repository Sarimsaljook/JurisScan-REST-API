from django.db import models


class UserFile(models.Model):
    user_id = models.CharField(max_length=100)
    file = models.FileField(upload_to='user_files/')
