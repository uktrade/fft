# Generated by Django 2.2 on 2019-06-21 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chartofaccountDIT", "0043_delete_budgettype")]

    operations = [
        migrations.CreateModel(
            name="BudgetType",
            fields=[
                (
                    "budget_type_key",
                    models.CharField(
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "budget_type",
                    models.CharField(max_length=100, verbose_name="Budget Type"),
                ),
            ],
        )
    ]