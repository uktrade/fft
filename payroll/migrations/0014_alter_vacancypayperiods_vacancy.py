# Generated by Django 4.2.16 on 2024-11-27 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0013_vacancy_fte_alter_vacancy_grade_vacancypayperiods_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vacancypayperiods",
            name="vacancy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pay_periods",
                to="payroll.vacancy",
            ),
        ),
    ]