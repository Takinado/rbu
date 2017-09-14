# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='time',
            field=models.TimeField(default=None, verbose_name='время'),
        ),
        migrations.AlterField(
            model_name='status',
            name='date',
            field=models.DateField(verbose_name='дата'),
        ),
    ]
