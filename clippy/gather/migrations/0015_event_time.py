# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gather', '0014_auto_20171030_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Enter a time for the event'),
            preserve_default=False,
        ),
    ]
