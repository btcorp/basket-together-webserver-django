# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-01 09:11
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160629_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=accounts.models.PhoneNumberField(blank=True, max_length=12, validators=[accounts.models.phonenumber_validator, accounts.models.phonenumber_validator, accounts.models.phonenumber_validator]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(blank=True, upload_to='%Y/%m/%d'),
        ),
    ]
