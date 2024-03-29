import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0006_data_20200810"),
        ("chartofaccountDIT", "0004_auto_20200820_0751"),
        ("costcentre", "0003_auto_20200824_1349"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("forecast", "0004_auto_20200820_0751"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArchivedFinancialCode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("archived", models.DateTimeField(auto_now_add=True)),
                (
                    "analysis1_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.ArchivedAnalysis1",
                    ),
                ),
                (
                    "analysis2_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.ArchivedAnalysis2",
                    ),
                ),
                (
                    "cost_centre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="costcentre.ArchivedCostCentre",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="previous_years_archivedfinancialcode",
                        to="core.FinancialYear",
                    ),
                ),
                (
                    "forecast_expenditure_type",
                    models.ForeignKey(
                        blank=True,
                        default=1,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="forecast.ForecastExpenditureType",
                    ),
                ),
                (
                    "natural_account_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.ArchivedNaturalCode",
                    ),
                ),
                (
                    "programme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.ArchivedProgrammeCode",
                    ),
                ),
                (
                    "project_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.ArchivedProjectCode",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SimpleHistoryArchivedForecastDataUpload",
            fields=[
                (
                    "id",
                    models.IntegerField(auto_created=True, blank=True, db_index=True),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                ("archived", models.DateTimeField(blank=True, editable=False)),
                ("budget", models.BigIntegerField(default=0)),
                ("apr", models.BigIntegerField(default=0)),
                ("may", models.BigIntegerField(default=0)),
                ("jun", models.BigIntegerField(default=0)),
                ("jul", models.BigIntegerField(default=0)),
                ("aug", models.BigIntegerField(default=0)),
                ("sep", models.BigIntegerField(default=0)),
                ("oct", models.BigIntegerField(default=0)),
                ("nov", models.BigIntegerField(default=0)),
                ("dec", models.BigIntegerField(default=0)),
                ("jan", models.BigIntegerField(default=0)),
                ("feb", models.BigIntegerField(default=0)),
                ("mar", models.BigIntegerField(default=0)),
                ("adj1", models.BigIntegerField(default=0)),
                ("adj2", models.BigIntegerField(default=0)),
                ("adj3", models.BigIntegerField(default=0)),
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
                    "financial_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="previous_years.ArchivedFinancialCode",
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
                        to="core.FinancialYear",
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
                "verbose_name": "historical archived forecast data upload",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="SimpleHistoryArchivedForecastData",
            fields=[
                (
                    "id",
                    models.IntegerField(auto_created=True, blank=True, db_index=True),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                ("archived", models.DateTimeField(blank=True, editable=False)),
                ("budget", models.BigIntegerField(default=0)),
                ("apr", models.BigIntegerField(default=0)),
                ("may", models.BigIntegerField(default=0)),
                ("jun", models.BigIntegerField(default=0)),
                ("jul", models.BigIntegerField(default=0)),
                ("aug", models.BigIntegerField(default=0)),
                ("sep", models.BigIntegerField(default=0)),
                ("oct", models.BigIntegerField(default=0)),
                ("nov", models.BigIntegerField(default=0)),
                ("dec", models.BigIntegerField(default=0)),
                ("jan", models.BigIntegerField(default=0)),
                ("feb", models.BigIntegerField(default=0)),
                ("mar", models.BigIntegerField(default=0)),
                ("adj1", models.BigIntegerField(default=0)),
                ("adj2", models.BigIntegerField(default=0)),
                ("adj3", models.BigIntegerField(default=0)),
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
                    "financial_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="previous_years.ArchivedFinancialCode",
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
                        to="core.FinancialYear",
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
                "verbose_name": "historical archived forecast data",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="SimpleHistoryArchivedFinancialCode",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                ("archived", models.DateTimeField(blank=True, editable=False)),
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
                    "analysis1_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.ArchivedAnalysis1",
                    ),
                ),
                (
                    "analysis2_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.ArchivedAnalysis2",
                    ),
                ),
                (
                    "cost_centre",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="costcentre.ArchivedCostCentre",
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
                        to="core.FinancialYear",
                    ),
                ),
                (
                    "forecast_expenditure_type",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        default=1,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="forecast.ForecastExpenditureType",
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
                (
                    "natural_account_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.ArchivedNaturalCode",
                    ),
                ),
                (
                    "programme",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.ArchivedProgrammeCode",
                    ),
                ),
                (
                    "project_code",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.ArchivedProjectCode",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical archived financial code",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="ArchivedForecastDataUpload",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("archived", models.DateTimeField(auto_now_add=True)),
                ("budget", models.BigIntegerField(default=0)),
                ("apr", models.BigIntegerField(default=0)),
                ("may", models.BigIntegerField(default=0)),
                ("jun", models.BigIntegerField(default=0)),
                ("jul", models.BigIntegerField(default=0)),
                ("aug", models.BigIntegerField(default=0)),
                ("sep", models.BigIntegerField(default=0)),
                ("oct", models.BigIntegerField(default=0)),
                ("nov", models.BigIntegerField(default=0)),
                ("dec", models.BigIntegerField(default=0)),
                ("jan", models.BigIntegerField(default=0)),
                ("feb", models.BigIntegerField(default=0)),
                ("mar", models.BigIntegerField(default=0)),
                ("adj1", models.BigIntegerField(default=0)),
                ("adj2", models.BigIntegerField(default=0)),
                ("adj3", models.BigIntegerField(default=0)),
                (
                    "financial_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="previous_years.ArchivedFinancialCode",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.FinancialYear",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("financial_code", "financial_year")},
            },
        ),
        migrations.CreateModel(
            name="ArchivedForecastData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("archived", models.DateTimeField(auto_now_add=True)),
                ("budget", models.BigIntegerField(default=0)),
                ("apr", models.BigIntegerField(default=0)),
                ("may", models.BigIntegerField(default=0)),
                ("jun", models.BigIntegerField(default=0)),
                ("jul", models.BigIntegerField(default=0)),
                ("aug", models.BigIntegerField(default=0)),
                ("sep", models.BigIntegerField(default=0)),
                ("oct", models.BigIntegerField(default=0)),
                ("nov", models.BigIntegerField(default=0)),
                ("dec", models.BigIntegerField(default=0)),
                ("jan", models.BigIntegerField(default=0)),
                ("feb", models.BigIntegerField(default=0)),
                ("mar", models.BigIntegerField(default=0)),
                ("adj1", models.BigIntegerField(default=0)),
                ("adj2", models.BigIntegerField(default=0)),
                ("adj3", models.BigIntegerField(default=0)),
                (
                    "financial_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="previous_years.ArchivedFinancialCode",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.FinancialYear",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "unique_together": {("financial_code", "financial_year")},
            },
        ),
    ]
