# Generated by Django 2.2.10 on 2020-04-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifthospitality', '0039_auto_20200408_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftandhospitality',
            name='rep_fk',
        ),
        migrations.RemoveField(
            model_name='simplehistorygiftandhospitality',
            name='rep_fk',
        ),
        migrations.AlterField(
            model_name='giftandhospitality',
            name='rep',
            field=models.CharField(blank=True, max_length=200, verbose_name='DIT representative offered to/from'),
        ),
        migrations.AlterField(
            model_name='simplehistorygiftandhospitality',
            name='rep',
            field=models.CharField(blank=True, max_length=200, verbose_name='DIT representative offered to/from'),
        ),
    ]