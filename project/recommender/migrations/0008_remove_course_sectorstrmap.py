# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 09:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_auto_20161125_0406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='sectorStrMap',
        ),
    ]
