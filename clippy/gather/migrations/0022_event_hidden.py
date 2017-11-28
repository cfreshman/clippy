# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-10 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gather', '0021_auto_20171107_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hidden',
            field=models.ManyToManyField(blank=True, help_text='These users have hidden the Event', related_name='hidden', to='gather.Profile'),
        ),
    ]