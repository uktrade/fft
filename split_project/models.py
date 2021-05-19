from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_pivot.pivot import pivot

from core.metamodels import BaseModel
from core.models import FinancialYear

from forecast.models import FinancialCode, FinancialPeriod

from previous_years.models import ArchivedFinancialCode


class ProjectSplitCoefficientAbstract(BaseModel):
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    financial_code_from = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="from_%(app_label)s_%(class)ss",
    )
    financial_code_to = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )
    # The coefficient is passed as a percentage with 2 decimal places
    # store it as integer to avoid rounding problems
    split_coefficient = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)],
    )

    class Meta:
        abstract = True
        unique_together = (
            "financial_period",
            "financial_code_from",
            "financial_code_to",
        )


class PreviousYearProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    financial_code_from = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.PROTECT,
        related_name="from_%(app_label)s_%(class)ss",
    )
    financial_code_to = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = (
            "financial_year",
            "financial_period",
            "financial_code_from",
            "financial_code_to",
        )


class PivotManager(models.Manager):
    """Managers returning the data in Monthly figures pivoted"""

    def pivot_data(self, columns, filter_dict={}, order_list=[]):

        q1 = self.get_queryset().filter(**filter_dict).order_by(*order_list)
        pivot_data = pivot(
            q1, columns, "financial_period__period_short_name", "split_coefficient",
        )
        return pivot_data


class ProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    objects = models.Manager()  # The default manager.
    pivot = PivotManager()
    permissions = [
        ("can_upload_files", "Can upload files"),
    ]


class UploadProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    row_number = models.IntegerField(default=0)
    pass


class TemporaryCalculatedValues(BaseModel):
    # temporary storage for the value calculated.
    financial_code = models.OneToOneField(FinancialCode, on_delete=models.CASCADE,)
    calculated_amount = models.BigIntegerField(null=True, blank=True)
