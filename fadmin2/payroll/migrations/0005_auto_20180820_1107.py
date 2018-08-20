# Generated by Django 2.0.2 on 2018-08-20 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costcentre', '0006_auto_20180820_1023'),
        ('payroll', '0004_auto_20180820_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='ditpeople',
            name='cost_centre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='costcentre.CostCentre'),
        ),
        migrations.AlterField(
            model_name='ditpeople',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ditpeople',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.Grade'),
        ),
    ]