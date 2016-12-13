# -*- coding:utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
import pytz


def change_timezone():
    seoul_tz = pytz.timezone('Asia/Seoul')
    datetime_format = "%Y-%m-%d %H:%M:%S"
    localized_time = timezone.now()
    return seoul_tz.normalize(localized_time).strftime(datetime_format)


class Post(models.Model):
    RECRUIT_STATUS = (
        (0, '모집중'),
        (1, '모집완료'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    registered_date = models.DateTimeField(default=change_timezone)
    recruit_count = models.IntegerField()
    attend_count = models.IntegerField(default=0)
    recruit_status = models.IntegerField(choices=RECRUIT_STATUS, default=0)   # 0:모집중, 1:모집완료
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    comment_count = models.IntegerField(default=0)
    latlng = models.CharField(max_length=50, blank=True)
    meeting_date = models.DateTimeField(default=change_timezone)

    class Meta:
        ordering = ('-registered_date',)

    def __str__(self):
        return self.title

    def registered_comments(self):
        return self.comments.filter(post=self.pk)

    @property
    def get_region_short_name(self):
        region = self.address1.split(' ')[0]
        if len(region) == 4:
            region_short_name = region[0]+region[2]
            return region_short_name
        else:
            return region[0:2]

    def as_json(self):
        return {
            'id': self.id,
            'author_id': self.author.id,
            'author_name': self.author.username,
            'title': self.title,
            'content': self.content,
            'recruit_count': self.recruit_count,
            'attend_list': self.participations.all(),
            'attend_count': self.attend_count,
            'comments': self.comments.all(),
            'comments_count': self.comments.all().count(),
            'registered_date': self.registered_date,
            'recruit_status': self.recruit_status,
            'meeting_date': self.meeting_date,
            'adress1': self.address1,
            'adress2': self.address2,
            'lat': self.lat,
            'lng': self.lng,
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
            return list(i.user.username for i in participations)
        else:
            return []

    def get_absolute_url(self):
        return reverse('recruit:post_detail', kwargs={'pk': self.pk})


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
            'author_id': self.author.id,
            'author_name': self.author.username,
            'registered_date': self.registered_date,
        }

    def get_absolute_url(self):
        return self.post.get_absolute_url()


class Participation(models.Model):
    post = models.ForeignKey(Post, related_name='participations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users')

    class Meta:
        unique_together = ('post', 'user', )

    def __str__(self):
        return self.post.title

    def as_json(self):
        return {
            'id': self.id,
            'post_id': self.post.id,
            'user_id': self.user.id,
            'user_name': self.user.username,
        }