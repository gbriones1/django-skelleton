# Generated by Django 3.0.1 on 2020-02-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20200223_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='method',
            field=models.CharField(choices=[('C', 'Efectivo'), ('T', 'Transferencia'), ('K', 'Cheque')], default='C', max_length=1, null=True),
        ),
    ]