# Generated by Django 3.0.1 on 2020-01-31 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20200130_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='number',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='sell',
            unique_together=set(),
        ),
    ]
