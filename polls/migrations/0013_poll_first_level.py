# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20160918_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='first_level',
            field=models.BooleanField(default=True),
        ),
    ]
