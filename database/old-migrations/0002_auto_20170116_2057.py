# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-16 20:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appliance',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['code']},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='storagetype',
            options={'ordering': ['name']},
        ),
    ]
