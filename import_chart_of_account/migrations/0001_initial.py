# Generated by Django 3.2.16 on 2023-04-12 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadNaturalCode",
            fields=[
                (
                    "natural_account_code",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="NAC"
                    ),
                ),
                (
                    "gross_income",
                    models.CharField(
                        blank=True,
                        choices=[("GR", "Gross"), ("IN", "Income")],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "cash_non_cash",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("CH", "Cash"),
                            ("NC", "Non-Cash"),
                            ("NA", "N/A Cash"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ["natural_account_code"],
            },
        ),
    ]