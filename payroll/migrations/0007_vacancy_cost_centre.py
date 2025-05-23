# Generated by Django 4.2.16 on 2024-11-13 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("costcentre", "0008_alter_simplehistoryarchivedcostcentre_options_and_more"),
        ("payroll", "0006_alter_vacancy_programme_switch_vacancy"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacancy",
            name="cost_centre",
            field=models.ForeignKey(
                default="888812",
                on_delete=django.db.models.deletion.PROTECT,
                to="costcentre.costcentre",
            ),
            preserve_default=False,
        ),
    ]
