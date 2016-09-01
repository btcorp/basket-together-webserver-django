# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-19 04:58
from __future__ import unicode_literals

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160718_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=accounts.models.PhoneNumberField(blank=True, max_length=12, validators=[accounts.models.phonenumber_validator, accounts.models.phonenumber_validator, accounts.models.phonenumber_validator]),
        ),
    ]