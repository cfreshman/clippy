# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gather', '0011_auto_20171029_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='images/user/placeholder.png', upload_to='images/user/'),
        ),
    ]
