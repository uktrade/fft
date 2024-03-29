# Generated by Django 3.2.4 on 2021-08-18 10:02

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chartofaccountDIT", "0011_auto_20210430_0925"),
        ("core", "0011_alter_historicaluser_first_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("treasurySS", "0003_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="simplehistoryorganizationcode",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="SimpleHistoryArchivedSubSegment",
            fields=[
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                ("archived", models.DateTimeField(blank=True, editable=False)),
                (
                    "sub_segment_code",
                    models.CharField(
                        db_index=True, max_length=8, verbose_name="sub segment code"
                    ),
                ),
                (
                    "sub_segment_long_name",
                    models.CharField(
                        max_length=255, verbose_name="sub segment long name"
                    ),
                ),
                (
                    "control_budget_detail_code",
                    models.CharField(
                        choices=[
                            (
                                "DEL",
                                (("DEL ADMIN", "DEL ADMIN"), ("DEL PROG", "DEL PROG")),
                            ),
                            ("NON-BUDGET", "NON-BUDGET"),
                            (
                                "AME",
                                (
                                    ("DEPT AME", "DEPT AME"),
                                    ("NON-DEPT AME", "NON-DEPT AME"),
                                ),
                            ),
                        ],
                        default="NON-BUDGET",
                        max_length=50,
                        verbose_name="control budget detail code",
                    ),
                ),
                (
                    "accounting_authority_code",
                    models.CharField(
                        max_length=255, verbose_name="accounting authority code"
                    ),
                ),
                (
                    "accounting_authority_DetailCode",
                    models.CharField(
                        choices=[
                            ("VT", "VOTED"),
                            (
                                "NVT",
                                (
                                    ("NON - VOTED_DEPT", "NON - VOTED_DEPT"),
                                    ("NON-VOTED_CFER", "NON-VOTED_CFER"),
                                    ("NON-VOTED_CF", "NON-VOTED_CF"),
                                    ("NON-VOTED_PC", "NON-VOTED_PC"),
                                    ("NON-VOTED_NIF", "NON-VOTED_NIF"),
                                    ("NON-VOTED_NLF", "NON-VOTED_NLF"),
                                    ("NON-VOTED_CEX", "NON-VOTED_CEX"),
                                    ("NON-VOTED_SF", "NON-VOTED_SF"),
                                    ("NON-VOTED_LG", "NON-VOTED_LG"),
                                    ("NON-VOTED_DA", "NON-VOTED_DA"),
                                ),
                            ),
                            ("N/A", "N/A"),
                        ],
                        default="N/A",
                        max_length=255,
                        verbose_name="accounting authority detail code",
                    ),
                ),
                (
                    "segment_grand_parent_code",
                    models.CharField(
                        max_length=8, verbose_name="segment grand parent code"
                    ),
                ),
                (
                    "segment_grand_parent_long_name",
                    models.CharField(
                        max_length=255, verbose_name="segment grandparent long name"
                    ),
                ),
                (
                    "segment_department_code",
                    models.CharField(
                        default="",
                        max_length=20,
                        verbose_name="segment department code",
                    ),
                ),
                (
                    "segment_department_long_name",
                    models.CharField(
                        default="",
                        max_length=255,
                        verbose_name="segment department long name",
                    ),
                ),
                (
                    "segment_parent_code",
                    models.CharField(max_length=8, verbose_name="segment parent code"),
                ),
                (
                    "segment_parent_long_name",
                    models.CharField(
                        max_length=255, verbose_name="segment parent long name"
                    ),
                ),
                (
                    "segment_code",
                    models.CharField(max_length=8, verbose_name="segment code"),
                ),
                (
                    "segment_long_name",
                    models.CharField(max_length=255, verbose_name="segment long name"),
                ),
                (
                    "organization_code",
                    models.CharField(max_length=50, verbose_name="Organization"),
                ),
                (
                    "organization_alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "estimate_row_code",
                    models.CharField(max_length=8, verbose_name="estimates row code"),
                ),
                (
                    "estimate_row_long_name",
                    models.CharField(
                        max_length=255, verbose_name="estimates row long name"
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
                    "dit_budget_type",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="chartofaccountDIT.budgettype",
                        verbose_name="DIT Budget Code (used to generate the Oscar return)",
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
                "verbose_name": "historical Archived Treasury Segments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="ArchivedSubSegment",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("archived", models.DateTimeField(auto_now_add=True)),
                (
                    "sub_segment_code",
                    models.CharField(
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                        verbose_name="sub segment code",
                    ),
                ),
                (
                    "sub_segment_long_name",
                    models.CharField(
                        max_length=255, verbose_name="sub segment long name"
                    ),
                ),
                (
                    "control_budget_detail_code",
                    models.CharField(
                        choices=[
                            (
                                "DEL",
                                (("DEL ADMIN", "DEL ADMIN"), ("DEL PROG", "DEL PROG")),
                            ),
                            ("NON-BUDGET", "NON-BUDGET"),
                            (
                                "AME",
                                (
                                    ("DEPT AME", "DEPT AME"),
                                    ("NON-DEPT AME", "NON-DEPT AME"),
                                ),
                            ),
                        ],
                        default="NON-BUDGET",
                        max_length=50,
                        verbose_name="control budget detail code",
                    ),
                ),
                (
                    "accounting_authority_code",
                    models.CharField(
                        max_length=255, verbose_name="accounting authority code"
                    ),
                ),
                (
                    "accounting_authority_DetailCode",
                    models.CharField(
                        choices=[
                            ("VT", "VOTED"),
                            (
                                "NVT",
                                (
                                    ("NON - VOTED_DEPT", "NON - VOTED_DEPT"),
                                    ("NON-VOTED_CFER", "NON-VOTED_CFER"),
                                    ("NON-VOTED_CF", "NON-VOTED_CF"),
                                    ("NON-VOTED_PC", "NON-VOTED_PC"),
                                    ("NON-VOTED_NIF", "NON-VOTED_NIF"),
                                    ("NON-VOTED_NLF", "NON-VOTED_NLF"),
                                    ("NON-VOTED_CEX", "NON-VOTED_CEX"),
                                    ("NON-VOTED_SF", "NON-VOTED_SF"),
                                    ("NON-VOTED_LG", "NON-VOTED_LG"),
                                    ("NON-VOTED_DA", "NON-VOTED_DA"),
                                ),
                            ),
                            ("N/A", "N/A"),
                        ],
                        default="N/A",
                        max_length=255,
                        verbose_name="accounting authority detail code",
                    ),
                ),
                (
                    "segment_grand_parent_code",
                    models.CharField(
                        max_length=8, verbose_name="segment grand parent code"
                    ),
                ),
                (
                    "segment_grand_parent_long_name",
                    models.CharField(
                        max_length=255, verbose_name="segment grandparent long name"
                    ),
                ),
                (
                    "segment_department_code",
                    models.CharField(
                        default="",
                        max_length=20,
                        verbose_name="segment department code",
                    ),
                ),
                (
                    "segment_department_long_name",
                    models.CharField(
                        default="",
                        max_length=255,
                        verbose_name="segment department long name",
                    ),
                ),
                (
                    "segment_parent_code",
                    models.CharField(max_length=8, verbose_name="segment parent code"),
                ),
                (
                    "segment_parent_long_name",
                    models.CharField(
                        max_length=255, verbose_name="segment parent long name"
                    ),
                ),
                (
                    "segment_code",
                    models.CharField(max_length=8, verbose_name="segment code"),
                ),
                (
                    "segment_long_name",
                    models.CharField(max_length=255, verbose_name="segment long name"),
                ),
                (
                    "organization_code",
                    models.CharField(max_length=50, verbose_name="Organization"),
                ),
                (
                    "organization_alias",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "estimate_row_code",
                    models.CharField(max_length=8, verbose_name="estimates row code"),
                ),
                (
                    "estimate_row_long_name",
                    models.CharField(
                        max_length=255, verbose_name="estimates row long name"
                    ),
                ),
                (
                    "dit_budget_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="chartofaccountDIT.budgettype",
                        verbose_name="DIT Budget Code (used to generate the Oscar return)",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="treasuryss_historicsubsegment",
                        to="core.financialyear",
                    ),
                ),
            ],
            options={
                "verbose_name": "Archived Treasury Segments",
                "unique_together": {
                    ("segment_code", "dit_budget_type", "financial_year")
                },
            },
        ),
    ]
