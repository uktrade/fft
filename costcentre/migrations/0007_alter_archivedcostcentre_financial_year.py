# Generated by Django 4.2.11 on 2024-03-18 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_auto_20220427_1046"),
        ("costcentre", "0006_auto_20230428_1106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="archivedcostcentre",
            name="financial_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s",
                to="core.financialyear",
            ),
        ),
    ]
