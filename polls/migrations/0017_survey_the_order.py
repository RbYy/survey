# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_charchoice_the_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
