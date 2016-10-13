# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 14:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0053_auto_20161013_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
