# Generated by Django 2.0.2 on 2018-08-28 09:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('costcentre', '0002_auto_20180821_1231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programme',
            old_name='DIT_in_use',
            new_name='active',
        ),
    ]