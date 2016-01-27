# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(max_length=254, null=True)),
                ('password', models.CharField(max_length=30, null=True)),
                ('receiver_email', models.EmailField(max_length=254, null=True)),
                ('mailOnPriceChange', models.BooleanField(default=True)),
                ('mailOnNegativeValues', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Input_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('input_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Input')),
            ],
        ),
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('returned', models.BooleanField(default=False)),
                ('returned_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lending_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('returned_amount', models.IntegerField()),
                ('lending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Lending')),
            ],
        ),
        migrations.CreateModel(
            name='Lending_Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('returned_amount', models.IntegerField()),
                ('lending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Lending')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('claimant', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('P', 'Por pedir'), ('A', 'Pedido'), ('C', 'Cancelado'), ('R', 'Recibido')], max_length=1, null=True)),
                ('received_date', models.DateTimeField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization_Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Movement')),
                ('replacer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Output_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('output_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Output')),
            ],
        ),
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_price_limit', models.DecimalField(decimal_places=2, max_digits=9)),
                ('percentage_1', models.DecimalField(decimal_places=2, max_digits=9)),
                ('percentage_2', models.DecimalField(decimal_places=2, max_digits=9)),
                ('percentage_3', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('appliance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Appliance')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Storage_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('organization_storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization_Storage')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Storage_Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('organization_storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization_Storage')),
            ],
        ),
        migrations.CreateModel(
            name='StorageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('condition', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='storage_tool',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Tool'),
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Provider'),
        ),
        migrations.AddField(
            model_name='output_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product'),
        ),
        migrations.AddField(
            model_name='organization_storage',
            name='products',
            field=models.ManyToManyField(through='warehouse.Storage_Product', to='warehouse.Product'),
        ),
        migrations.AddField(
            model_name='organization_storage',
            name='storage_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.StorageType'),
        ),
        migrations.AddField(
            model_name='organization_storage',
            name='tools',
            field=models.ManyToManyField(through='warehouse.Storage_Tool', to='warehouse.Tool'),
        ),
        migrations.AddField(
            model_name='order_product',
            name='organization_storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization_Storage'),
        ),
        migrations.AddField(
            model_name='order_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Provider'),
        ),
        migrations.AddField(
            model_name='movement',
            name='organization_storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Organization_Storage'),
        ),
        migrations.AddField(
            model_name='lending_tool',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Tool'),
        ),
        migrations.AddField(
            model_name='lending_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product'),
        ),
        migrations.AddField(
            model_name='lending',
            name='movement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Movement'),
        ),
        migrations.AddField(
            model_name='input_product',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product'),
        ),
        migrations.AddField(
            model_name='input',
            name='movement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Movement'),
        ),
    ]
