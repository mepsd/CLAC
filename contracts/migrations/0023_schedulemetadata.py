# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-19 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0022_remove_piid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(db_index=True, help_text='Text that appears in the "schedule" column of Contract data to identify a labor rate as being in this schedule (e.g. "MOBIS").', max_length=128, unique=True)),
                ('sin', models.CharField(help_text='The SIN number for the schedule (e.g. "874").', blank=True, max_length=128)),
                ('name', models.CharField(help_text='The name of the schedule as it should appear to CALC users (e.g. "Legacy MOBIS").', max_length=128)),
                ('description', models.TextField(help_text='A description of the schedule, formatted as Markdown.')),
            ],
        ),
    ]
