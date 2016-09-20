# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_charchoice_nested'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='charchoice',
            name='nested',
            field=models.ManyToManyField(blank=True, related_name='nesting_choices', to='polls.Poll'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.CharField(choices=[('multi', 'pick multiple options'), ('one', 'pick one option'), ('countries', 'pick a country from the list'), ('text', 'type text'), ('email_now', 'email - save and send at Submit'), ('email', 'email - just save')], default='multi', max_length=30),
        ),
        migrations.AlterField(
            model_name='poll',
            name='survey',
            field=models.ManyToManyField(blank=True, to='polls.Survey'),
        ),
    ]