# Generated by Django 3.0.1 on 2021-07-05 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_movement_evidence'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storage_product',
            unique_together={('organization_storage', 'product')},
        ),
    ]