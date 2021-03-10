from django.db import models
from django.db.models import (
    Q,
    UniqueConstraint,
)

from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.metamodels import (
    ArchivedModel,
)
from core.models import FinancialYear

from costcentre.models import ArchivedCostCentre

from forecast.models import (
    FinancialCodeAbstract,
    ForecastExpenditureType,
    ForecastingDataViewAbstract,
    MonthlyFigureAbstract,
)


class ArchivedFinancialCode(ArchivedModel, FinancialCodeAbstract):
    """Contains the members of Chart of Account needed to create a unique key"""

    programme = models.ForeignKey(ArchivedProgrammeCode, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(ArchivedCostCentre, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(
        ArchivedNaturalCode, on_delete=models.PROTECT
    )
    analysis1_code = models.ForeignKey(
        ArchivedAnalysis1, on_delete=models.PROTECT, blank=True, null=True
    )
    analysis2_code = models.ForeignKey(
        ArchivedAnalysis2, on_delete=models.PROTECT, blank=True, null=True
    )
    project_code = models.ForeignKey(
        ArchivedProjectCode, on_delete=models.PROTECT, blank=True, null=True
    )

    forecast_expenditure_type = models.ForeignKey(
        ForecastExpenditureType,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        null=True,
    )

    class Meta:
        # Several constraints required, to cover all the permutations of
        # fields that can be Null
        constraints = [
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis1_code",
                    "analysis2_code",
                    "project_code",
                ],
                name="archived_financial_row_unique_6",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis2_code",
                    "project_code",
                ],
                name="archived_financial_row_unique_5a",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis1_code",
                    "project_code",
                ],
                name="archived_financial_row_unique_5b",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis1_code",
                    "analysis2_code",
                ],
                name="archived_financial_row_unique_5c",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "project_code",
                ],
                name="archived_financial_row_unique_4a",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis1_code",
                ],
                name="archived_financial_row_unique_4b",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                    "analysis2_code",
                ],
                name="archived_financial_row_unique_4c",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=["programme", "cost_centre", "natural_account_code", ],
                name="archived_financial_row_unique_3",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=True),
            ),
        ]


class ArchivedForecastDataAbstract(ForecastingDataViewAbstract, ArchivedModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    financial_code = models.ForeignKey(ArchivedFinancialCode, on_delete=models.PROTECT,)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)

    class Meta:
        abstract = True
        unique_together = ("financial_code", "financial_year")


class ArchivedForecastDataUpload(ArchivedForecastDataAbstract):
    pass


class ArchivedForecastData(ArchivedForecastDataAbstract):
    pass


class ArchivedActualUploadMonthlyFigure(MonthlyFigureAbstract):
    financial_code = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["financial_code", "financial_year", "financial_period", ],
                name="ArchivedActualUploadMonthlyFigure_unique1",
            ),
        ]
