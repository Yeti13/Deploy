# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_app', '0002_auto_20170528_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secrets',
            name='likes',
            field=models.IntegerField(),
        ),
    ]
