# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20160918_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='charchoice',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
