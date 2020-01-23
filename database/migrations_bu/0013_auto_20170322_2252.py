# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-22 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20170314_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xxx', to='database.Product'),
        ),
        migrations.AlterField(
            model_name='output',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Customer'),
        ),
    ]