# Generated by Django 2.2.13 on 2020-08-28 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chartofaccountDIT", "0004_auto_20200820_0751"),
    ]

    operations = [
        migrations.RenameField(
            model_name="archivednaturalcode",
            old_name="expenditure_category",
            new_name="expenditure_category_description",
        ),
        migrations.RenameField(
            model_name="simplehistoryarchivednaturalcode",
            old_name="expenditure_category",
            new_name="expenditure_category_description",
        ),
        migrations.AddField(
            model_name="archivednaturalcode",
            name="expenditure_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.ArchivedExpenditureCategory",
                verbose_name="Budget Category",
            ),
        ),
        migrations.AddField(
            model_name="simplehistoryarchivednaturalcode",
            name="expenditure_category",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="chartofaccountDIT.ArchivedExpenditureCategory",
                verbose_name="Budget Category",
            ),
        ),
        migrations.RunSQL(
            'update "chartofaccountDIT_archivednaturalcode" SET expenditure_category_id = a.id '
            'FROM "chartofaccountDIT_archivedexpenditurecategory" a  '
            'WHERE a.grouping_description = "chartofaccountDIT_archivednaturalcode".expenditure_category_description '
            'AND a.financial_year_id = "chartofaccountDIT_archivednaturalcode".financial_year_id'
        ),
        migrations.RenameField(
            model_name="archivedexpenditurecategory",
            old_name="NAC_category",
            new_name="NAC_category_description",
        ),
        migrations.RenameField(
            model_name="simplehistoryarchivedexpenditurecategory",
            old_name="NAC_category",
            new_name="NAC_category_description",
        ),
        migrations.AddField(
            model_name="archivedexpenditurecategory",
            name="NAC_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="chartofaccountDIT.NACCategory",
                verbose_name="Budget Grouping",
            ),
        ),
        migrations.AddField(
            model_name="simplehistoryarchivedexpenditurecategory",
            name="NAC_category",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="chartofaccountDIT.NACCategory",
                verbose_name="Budget Grouping",
            ),
        ),
        migrations.RunSQL(
            'update "chartofaccountDIT_archivedexpenditurecategory" '
            'SET "NAC_category_id" = a.id '
            'FROM "chartofaccountDIT_naccategory" a '
            'WHERE a."NAC_category_description" = '
            '"chartofaccountDIT_archivedexpenditurecategory"."NAC_category_description";'
        ),
    ]
