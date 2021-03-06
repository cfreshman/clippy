# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gather', '0009_auto_20171029_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(upload_to='images/event/'),
        ),
        migrations.AlterField(
            model_name='group',
            name='images',
            field=models.ImageField(upload_to='images/group/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='images/user/Default.jpg', upload_to='images/user/'),
        ),
    ]
