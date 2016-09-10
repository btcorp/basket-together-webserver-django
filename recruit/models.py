# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from django.conf import settings
import pytz

RECRUIT_STATUS = (
    (0, ),
    (),
)


def change_timezone():
    seoul_tz = pytz.timezone('Asia/Seoul')
    datetime_format = "%Y-%m-%d %H:%M:%S"
    localized_time = timezone.now()
    return seoul_tz.normalize(localized_time).strftime(datetime_format)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    registered_date = models.DateTimeField(default=change_timezone)
    recruit_count = models.IntegerField()
    attend_count = models.IntegerField(default=1)
    recruit_status = models.CharField(max_length=1, default='0')   # 0:모집중, 1:모집완료
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    comment_count = models.IntegerField(default=0)
    latlng = models.CharField(max_length=50, blank=True, default='37.497921,127.027636')
    meeting_date = models.DateTimeField(default=change_timezone)

    def __str__(self):
        return self.title

    def registered_comments(self):
        return self.comments.filter(post=self.pk)

    def as_json(self):
        return {
            'id': self.id,
            'author_id': self.author.id,
            'author_name': self.author.username,
            'title': self.title,
            'content': self.content,
            'recruit_count': self.recruit_count,
            'attend_count': self.attend_count,
            'comments': self.comments.all(),
            'comments_count': self.comments.all().count(),
            'registered_date': self.registered_date,
            'recruit_status': self.recruit_status,
        }

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

    def attend_users(self):
        participations = Participation.objects.filter(post=self)
        if participations:
            return list(i.user.email for i in participations)
        else:
            return []


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    registered_date = models.DateTimeField(default=change_timezone)

    def __str__(self):
        return self.content

    def as_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'registered_date': self.registered_date,

        }


class Participation(models.Model):
    post = models.ForeignKey(Post, related_name='participations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users')

    def __str__(self):
        return self.post.title
