# Generated by Django 3.2.7 on 2021-12-09 11:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("previous_years", "0004_auto_20210707_1008"),
        ("forecast", "0008_amend_views_20210802_1439"),
        ("core", "0011_alter_historicaluser_first_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimpleHistoryUploadPaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                ("row_number", models.IntegerField(default=0)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.financialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.financialperiod",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical upload pay split coefficient",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="SimpleHistoryPreviousYearPaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="previous_years.archivedfinancialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.financialperiod",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="core.financialyear",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical previous year pay split coefficient",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="SimpleHistoryPaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.financialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.financialperiod",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical pay split coefficient",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="UploadPaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                ("row_number", models.IntegerField(default=0)),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="to_upload_split_file_uploadpaysplitcoefficients",
                        to="forecast.financialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="upload_split_file_uploadpaysplitcoefficients",
                        to="forecast.financialperiod",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("financial_period", "financial_code_to")},
            },
        ),
        migrations.CreateModel(
            name="PreviousYearPaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="to_upload_split_file_previousyearpaysplitcoefficients",
                        to="previous_years.archivedfinancialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="upload_split_file_previousyearpaysplitcoefficients",
                        to="forecast.financialperiod",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.financialyear",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("financial_year", "financial_period", "financial_code_to")
                },
            },
        ),
        migrations.CreateModel(
            name="PaySplitCoefficient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "directorate_code",
                    models.CharField(max_length=6, verbose_name="Directorate Code"),
                ),
                (
                    "split_coefficient",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                (
                    "financial_code_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="to_upload_split_file_paysplitcoefficients",
                        to="forecast.financialcode",
                    ),
                ),
                (
                    "financial_period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="upload_split_file_paysplitcoefficients",
                        to="forecast.financialperiod",
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_upload_percentage_files", "Can upload percentage files")
                ],
                "abstract": False,
                "unique_together": {("financial_period", "financial_code_to")},
            },
        ),
    ]