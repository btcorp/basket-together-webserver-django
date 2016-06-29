from django.db import models
from django.utils import timezone
from django import forms

RECRUIT_STATUS = (
    (0, ),
    (),
)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    content = models.TextField()
    registered_date = models.DateTimeField(default=timezone.now)
    recruit_count = models.IntegerField()
    attend_count = models.IntegerField(default=0)
    recruit_status = models.CharField(max_length=20, default='ing')
    gps_x = models.CharField(max_length=20)
    gps_y = models.CharField(max_length=20)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    comment_count = models.IntegerField(default=0)
    latlng = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def registered_comments(self):
        return self.comments.filter(post=self.pk)

    @property
    def lat(self):
        if self.latlng:
            return self.latlng.split(',')[0]
        return None

    @property
    def lng(self):
        if self.latlng:
            return self.latlng.split(',')[1]
        return None


class Comment(models.Model):
    post = models.ForeignKey('recruit.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    content = models.TextField()
    registered_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
