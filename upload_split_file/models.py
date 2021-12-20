from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_pivot.pivot import pivot

from core.metamodels import BaseModel
from core.models import FinancialYear

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    MonthlyFigureAbstract,
)


from previous_years.models import ArchivedFinancialCode


class PaySplitCoefficientAbstract(BaseModel):
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    financial_code_to = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )
    # Added for convenience. Used to calculate the Pay to be split
    directorate_code = models.CharField("Directorate Code", max_length=6)
    # The coefficient is passed as a percentage with 2 decimal places
    # store it as integer to avoid rounding problems
    split_coefficient = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)],
    )

    class Meta:
        abstract = True
        unique_together = (
            "financial_period",
            "financial_code_to",
        )


class PreviousYearPaySplitCoefficient(PaySplitCoefficientAbstract):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    financial_code_to = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = (
            "financial_year",
            "financial_period",
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


class PaySplitCoefficient(PaySplitCoefficientAbstract):
    objects = models.Manager()  # The default manager.
    pivot = PivotManager()

    class Meta(PaySplitCoefficientAbstract.Meta):
        permissions = [
            ("can_upload_percentage_files", "Can upload percentage files"),
        ]


class UploadPaySplitCoefficient(PaySplitCoefficientAbstract):
    row_number = models.IntegerField(default=0)


class TemporaryCalculatedValues(BaseModel):
    # temporary storage for the value calculated.
    financial_code = models.OneToOneField(FinancialCode, on_delete=models.CASCADE,)
    calculated_amount = models.BigIntegerField(null=True, blank=True)


class SplitPayActualFigure(MonthlyFigureAbstract):
    # Used to store the actual after they have been split
    # using the percentage in PaySplitCoefficient
    # This data is not used in FFT, it is passed to the data lake
    # where the report is created
    pass
