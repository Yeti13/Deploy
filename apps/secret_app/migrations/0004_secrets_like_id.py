# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_app', '0003_auto_20170529_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='secrets',
            name='like_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
