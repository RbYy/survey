# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0028_auto_20160921_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dicty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='KeyVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(default=0, max_length=150)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Dicty')),
            ],
        ),
        migrations.AddField(
            model_name='surveyattribute',
            name='dicti',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Dicty'),
        ),
    ]
