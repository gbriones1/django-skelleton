# Generated by Django 3.0.1 on 2021-09-27 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_auto_20210705_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Organization'),
        ),
    ]
