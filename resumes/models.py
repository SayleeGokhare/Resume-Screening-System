from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    skills = models.TextField(blank=True)
    content = models.TextField(blank=True)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
