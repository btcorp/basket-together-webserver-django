from django.db import models
from django.conf import settings


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.message