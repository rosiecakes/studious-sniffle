# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 01:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160903_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='tasks',
        ),
    ]
