import re
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

DEVICE_TYPE=(
    ('a', 'ANDROID'),
    ('i', 'IOS'),
)


def phonenumber_validator(value):
    if re.match(r'^01[016789][1-9]\d{6,7}$', value) is None:
        raise ValidationError('휴대폰 번호를 입력해주세요.')


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('validators', [])
        kwargs['validators'].append(phonenumber_validator)
        super(PhoneNumberField, self).__init__(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=12, blank=True)
    device_type = models.CharField(max_length=1, choices=DEVICE_TYPE, default='ANDROID')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True, default=0)
    penalty_count = models.IntegerField(blank=True, default=0)


User.profile = property(lambda user: Profile.objects.get_or_create(user=user)[0])

