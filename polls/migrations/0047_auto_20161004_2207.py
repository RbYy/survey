# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0046_auto_20161004_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charchoice',
            name='choice_text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='choicegroup',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
