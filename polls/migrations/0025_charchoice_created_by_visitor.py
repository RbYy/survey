# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_auto_20160920_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='charchoice',
            name='created_by_visitor',
            field=models.BooleanField(default=True),
        ),
    ]
