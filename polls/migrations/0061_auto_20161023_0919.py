# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-23 09:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0060_auto_20161022_2058'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='surveypreferencemodel',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='surveypreferencemodel',
            name='instance',
        ),
        migrations.DeleteModel(
            name='SurveyPreferenceModel',
        ),
    ]