# -*- coding:utf-8 -*-

import re
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


DEVICE_TYPE = (
    ('a', 'ANDROID'),
    ('i', 'IOS'),
)


def phonenumber_validator(value):
    if re.match(r'^01[016789][1-9]\d{6,7}$', value) is None:
        raise ValidationError('휴대폰 번호를 입력해주세요.')


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('help_text', "'-' 없이 번호를 입력해주세요.")
        kwargs.setdefault('validators', [])
        kwargs['validators'].append(phonenumber_validator)
        super(PhoneNumberField, self).__init__(*args, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text=_('Required.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_admin = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=12, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE, default='ANDROID')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True, default=0)
    penalty_count = models.IntegerField(blank=True, default=0)
    user_image = models.ImageField(blank=True, upload_to='%Y/%m/%d')


class Friendship(models.Model):
    from_friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_friends')
    to_friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_friends')

    class Meta:
        unique_together = (('from_friend', 'to_friend'), )

    def __str__(self):
        return '{}, {}'.format(self.from_friend, self.to_friend)


CustomUser.profile = property(lambda user: Profile.objects.get_or_create(user=user)[0])

