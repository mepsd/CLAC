# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-06 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_capture', '0017_auto_20170316_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedpricelistrow',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submittedpricelistrow',
            name='certifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]
