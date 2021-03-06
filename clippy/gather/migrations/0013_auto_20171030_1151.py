# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gather', '0012_auto_20171029_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a brief description of the Event', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Groups this user is associated with', null=True, related_name='events', to='gather.Group'),
        ),
        migrations.AlterField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(blank=True, help_text='These users are invited to the event', null=True, related_name='invited', to='gather.User'),
        ),
        migrations.AlterField(
            model_name='event',
            name='joined',
            field=models.ManyToManyField(blank=True, help_text='These users have joined the Event', null=True, related_name='joined', to='gather.User'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, help_text='Location', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/event/'),
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a bried description of the group', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/group/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, help_text='Friends of this user', null=True, related_name='_user_friends_+', to='gather.User'),
        ),
    ]
