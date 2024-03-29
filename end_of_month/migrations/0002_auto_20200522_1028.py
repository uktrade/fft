# Generated by Django 2.2.10 on 2020-05-22 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forecast", "0001_initial"),
        ("end_of_month", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="endofmonthstatus",
            name="archived_period",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="end_of_month_endofmonthstatuss",
                to="forecast.FinancialPeriod",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="simplehistoryendofmonthstatus",
            name="archived_period",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forecast.FinancialPeriod",
            ),
        ),
    ]
