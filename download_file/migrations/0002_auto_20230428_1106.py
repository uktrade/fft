# Generated by Django 3.2.16 on 2023-04-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("download_file", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filedownload",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("Oscar Return", "OSCAR Return"),
                    ("Previous Year Oscar Return", "Previous Year Oscar Return"),
                    ("Forecast", "Forecast"),
                    ("Previous Year Actuals", "Previous Year Forecast/Actuals"),
                    ("Budget", "Budget"),
                ],
                default="Forecast",
                max_length=70,
            ),
        ),
        migrations.AlterField(
            model_name="simplehistoryfiledownload",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("Oscar Return", "OSCAR Return"),
                    ("Previous Year Oscar Return", "Previous Year Oscar Return"),
                    ("Forecast", "Forecast"),
                    ("Previous Year Actuals", "Previous Year Forecast/Actuals"),
                    ("Budget", "Budget"),
                ],
                default="Forecast",
                max_length=70,
            ),
        ),
    ]
