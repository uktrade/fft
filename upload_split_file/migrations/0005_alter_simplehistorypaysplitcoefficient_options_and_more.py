# Generated by Django 4.2.15 on 2024-10-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "upload_split_file",
            "0004_alter_paysplitcoefficient_financial_code_to_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="simplehistorypaysplitcoefficient",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical pay split coefficient",
                "verbose_name_plural": "historical pay split coefficients",
            },
        ),
        migrations.AlterModelOptions(
            name="simplehistorypreviousyearpaysplitcoefficient",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical previous year pay split coefficient",
                "verbose_name_plural": "historical previous year pay split coefficients",
            },
        ),
        migrations.AlterModelOptions(
            name="simplehistorysplitpayactualfigure",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical split pay actual figure",
                "verbose_name_plural": "historical split pay actual figures",
            },
        ),
        migrations.AlterModelOptions(
            name="simplehistorytemporarycalculatedvalues",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical temporary calculated values",
                "verbose_name_plural": "historical temporary calculated valuess",
            },
        ),
        migrations.AlterModelOptions(
            name="simplehistoryuploadpaysplitcoefficient",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical upload pay split coefficient",
                "verbose_name_plural": "historical upload pay split coefficients",
            },
        ),
        migrations.AlterField(
            model_name="simplehistorypaysplitcoefficient",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="simplehistorypreviousyearpaysplitcoefficient",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="simplehistorysplitpayactualfigure",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="simplehistorytemporarycalculatedvalues",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="simplehistoryuploadpaysplitcoefficient",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]