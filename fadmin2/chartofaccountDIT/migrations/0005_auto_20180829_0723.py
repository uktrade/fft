# Generated by Django 2.0.2 on 2018-08-29 07:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('chartofaccountDIT', '0004_auto_20180828_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis1',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='analysis2',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commercialcategory',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expenditurecategory',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='naccategory',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]