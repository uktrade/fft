# Generated by Django 5.1.5 on 2025-03-17 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gifthospitality", "0007_alter_grade_grade_alter_simplehistorygrade_grade"),
        ("payroll", "0020_alter_employee_grade_alter_vacancy_grade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="grade",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="gifthospitality.grade"
            ),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="grade",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="gifthospitality.grade"
            ),
        ),
    ]
