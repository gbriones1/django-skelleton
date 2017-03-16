# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-14 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20170307_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
