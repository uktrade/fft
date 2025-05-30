import copy
import hashlib
from typing import Self

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models import F, Max, Q, Sum, UniqueConstraint
from django.template.defaultfilters import slugify

# https://github.com/martsberger/django-pivot/blob/master/django_pivot/pivot.py
from django_pivot.pivot import pivot

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)
from core.metamodels import BaseModel
from core.models import FinancialYear
from core.utils.generic_helpers import (
    GRAND_TOTAL_CLASS,
    SUB_TOTAL_CLASS,
    TOTAL_CLASS,
    get_current_financial_year,
)
from costcentre.models import CostCentre
from forecast.utils.view_field_definition import (
    budget_field,
    outturn_field,
    outturn_variance_field,
)


GRAND_TOTAL_ROW = "grand_total"
MAX_PERIOD_CODE = 15


class SubTotalFieldDoesNotExistError(Exception):
    pass


class SubTotalFieldNotSpecifiedError(Exception):
    pass


class ForecastEditState(BaseModel):
    closed = models.BooleanField(
        default=False,
        help_text="Ticking this option will close editing access "
        "to all non finance staff. Forecast editing is still "
        "available to Finance business partners/BSCEs and admin.",
    )
    lock_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Lock system",
        help_text="The system is locked from the date entered. "
        "The system will remain locked to users without "
        "'unlocked' user status, until the date is removed "
        "from the input field above. Please remember to archive the "
        "data after locking the forecast.",
    )

    def __str__(self):
        return "Forecast edit state"

    class Meta:
        verbose_name_plural = "Forecast edit state"
        default_permissions = ("view", "change")
        permissions = [
            ("can_set_edit_lock", "Can set edit lock"),
            (
                "can_edit_whilst_closed",
                "Can edit forecasts whilst system is closed",
            ),
            (
                "can_edit_whilst_locked",
                "Can edit forecasts whilst system is locked",
            ),
        ]


class FutureForecastEditState(BaseModel):
    closed = models.BooleanField(
        default=False,
        help_text="Ticking this option will close future forecast editing access "
        "to all non finance staff. Future forecast editing is still "
        "available to Finance business partners/BSCEs and admin.",
    )
    lock_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Lock future forecast",
        help_text="The future forecast editing is locked from the date entered. "
        "The future forecast editing will remain locked to users without "
        "'unlocked' user status, until the date is removed "
        "from the input field above.",
    )

    def __str__(self):
        return "Future forecast edit state"

    class Meta:
        verbose_name_plural = "Future forecast edit state"
        default_permissions = ("view", "change")
        permissions = [
            ("can_set_future_edit_lock", "Can set future edit lock"),
            (
                "can_edit_future_whilst_closed",
                "Can edit future forecasts whilst system is closed",
            ),
            (
                "can_edit_future_whilst_locked",
                "Can edit future forecasts whilst system is locked",
            ),
        ]


class UnlockedForecastEditor(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="users"
    )

    def __str__(self):
        return str(self.user)


class ForecastExpenditureType(BaseModel):
    """The expenditure type is a combination of
    the economic budget (NAC) and the budget type (Programme).
    As such, it can only be defined for a forecast
    row, when both NAC and programme are defined.
    This table is prepopulated with the  information
    needed to get the expenditure_type.
    """

    nac_economic_budget_code = models.CharField(
        max_length=255, verbose_name="economic budget code"
    )
    programme_budget_type = models.ForeignKey(BudgetType, on_delete=models.CASCADE)

    forecast_expenditure_type_name = models.CharField(max_length=100)
    forecast_expenditure_type_description = models.CharField(max_length=100)
    forecast_expenditure_type_display_order = models.IntegerField()

    class Meta:
        unique_together = ("nac_economic_budget_code", "programme_budget_type")

    def __str__(self):
        return self.forecast_expenditure_type_name


class FinancialPeriodQuerySet(models.QuerySet):
    def months(self):
        """Filter by real months, excluding the 3 adjustment periods (13, 14, 15)."""
        return self.filter(financial_period_code__lte=12)


class FinancialPeriodManager(models.Manager):
    def month_display_list(self):
        return list(
            self.get_queryset()
            .filter(financial_period_code__lte=12)
            .values_list("period_short_name", flat=True)
        )

    def month_adj_display_list(self):
        return list(self.get_queryset().values_list("period_short_name", flat=True))

    def adj_display_list(self):
        return list(
            self.get_queryset()
            .filter(financial_period_code__gt=12, display_figure=True)
            .values_list("period_short_name", flat=True)
        )

    def all_adj_list(self):
        return list(
            self.get_queryset()
            .filter(financial_period_code__gt=12)
            .values_list("period_short_name", flat=True)
        )

    def period_display_list(self):
        return list(
            self.get_queryset()
            .filter(display_figure=True)
            .values_list("period_short_name", flat=True)
        )

    def period_display_all_list(self):
        return list(self.get_queryset().values_list("period_short_name", flat=True))

    def period_display_code_list(self):
        return list(
            self.get_queryset()
            .filter(display_figure=True)
            .values_list("financial_period_code", flat=True)
        )

    def month_sublist(self, month):
        if month > MAX_PERIOD_CODE:
            # needed for displaying previous year outturn
            month = MAX_PERIOD_CODE
        return self.period_display_list()[:month]

    def actual_month(self):
        # use the Max to protect us from the situation of
        # non contiguous actual month.
        aggregate_queryset = (
            self.get_queryset()
            .filter(actual_loaded=True)
            .aggregate(Max("financial_period_code"))
        )
        return aggregate_queryset["financial_period_code__max"] or 0

    def actual_period_code_list(self):
        last_actual_month = self.actual_month()
        return list(
            self.get_queryset()
            .filter(financial_period_code__lte=last_actual_month)
            .values_list(
                "financial_period_code",
                flat=True,
            )
        )

    def forecast_period_code_list(self):
        last_actual_month = self.actual_month()
        return list(
            self.get_queryset()
            .filter(financial_period_code__gt=last_actual_month)
            .values_list(
                "financial_period_code",
                flat=True,
            )
        )

    def actual_month_previous_year(self):
        # use the Max to protect us from the situation of
        # non contiguous actual month.
        m = (
            self.get_queryset()
            .filter(actual_loaded_previous_year=True)
            .aggregate(Max("financial_period_code"))
        )
        return m["financial_period_code__max"] or 0

    def actual_month_list(self):
        return self.month_sublist(self.actual_month())

    def actual_month_previous_year_list(self):
        # use period_display_all_list because adjustement (ADJxx) periods
        # must be included when showing  previous year data
        return self.period_display_all_list()[: self.actual_month_previous_year()]

    def periods(self):
        return (
            self.get_queryset()
            .filter(display_figure=True)
            .values_list("period_short_name", "period_long_name")
        )

    def month_periods(self):
        return (
            self.get_queryset()
            .filter(financial_period_code__lte=12)
            .values_list("period_short_name", "period_long_name")
        )

    def adj_periods(self):
        return (
            self.get_queryset()
            .filter(financial_period_code__gt=12, display_figure=True)
            .values_list("period_short_name", "period_long_name")
        )

    def reset_actuals(self):
        self.get_queryset().filter(actual_loaded=True).update(actual_loaded=False)

    def get_max_period(self):
        return self.get_queryset().order_by("-financial_period_code").first()


class FinancialPeriod(BaseModel):
    """Financial periods: correspond to month, but there are 3 extra periods at the end.

    There are 15 objects in total.

    The objects are managed in migrations and therefore always available in tests.
    """

    financial_period_code = models.IntegerField(primary_key=True)  # April = 1
    period_long_name = models.CharField(max_length=20)
    period_short_name = models.CharField(max_length=10)
    period_calendar_code = models.IntegerField()  # January = 1
    # use a flag to indicate if the "actuals"
    # have been uploaded instead of relying on the date
    # the "actuals" are manually uploaded, so it is not
    # guaranteed on which date they are uploaded
    actual_loaded = models.BooleanField(default=False)
    actual_loaded_previous_year = models.BooleanField(default=False)
    display_figure = models.BooleanField(default=True)

    objects = FinancialPeriodQuerySet.as_manager()
    financial_period_info = FinancialPeriodManager()

    class Meta:
        ordering = ["financial_period_code"]

    def __str__(self):
        return self.period_long_name


class FinancialCodeAbstract(models.Model):
    """Contains the members of Chart of Account needed to create a unique key"""

    class Meta:
        abstract = True
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
                name="financial_row_unique_6",
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
                name="financial_row_unique_5a",
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
                name="financial_row_unique_5b",
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
                name="financial_row_unique_5c",
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
                name="financial_row_unique_4a",
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
                name="financial_row_unique_4b",
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
                name="financial_row_unique_4c",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "programme",
                    "cost_centre",
                    "natural_account_code",
                ],
                name="financial_row_unique_3",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=True),
            ),
        ]
        permissions = [
            ("can_view_forecasts", "Can view forecast"),
            ("can_upload_files", "Can upload files"),
            ("can_download_oscar", "Can download OSCAR"),
            ("can_download_mi_reports", "Can download mi reports"),
        ]

    def save(self, *args, **kwargs):
        # Override save to calculate the forecast_expenditure_type.
        if self.pk is None or self.forecast_expenditure_type is None:
            # calculate the forecast_expenditure_type
            nac_economic_budget_code = self.natural_account_code.economic_budget_code
            programme_budget_type = self.programme.budget_type
            forecast_type = ForecastExpenditureType.objects.filter(
                programme_budget_type=programme_budget_type,
                nac_economic_budget_code__iexact=nac_economic_budget_code,
            )
            self.forecast_expenditure_type = forecast_type.first()

        super(FinancialCodeAbstract, self).save(*args, **kwargs)

    @property
    def is_locked(self) -> bool:
        if self.cost_centre.is_overseas:
            return False

        return (
            self.natural_account_code_id in settings.PAYROLL_NACS
            and self.analysis1_code is None
            and self.analysis2_code is None
            and self.project_code is None
        )


class FinancialCode(FinancialCodeAbstract, BaseModel):
    programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    analysis1_code = models.ForeignKey(
        Analysis1, on_delete=models.PROTECT, blank=True, null=True
    )
    analysis2_code = models.ForeignKey(
        Analysis2, on_delete=models.PROTECT, blank=True, null=True
    )
    project_code = models.ForeignKey(
        ProjectCode, on_delete=models.PROTECT, blank=True, null=True
    )
    # The following field is calculated from programme and NAC.
    forecast_expenditure_type = models.ForeignKey(
        ForecastExpenditureType,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        null=True,
    )

    def as_key(self, **kwargs) -> str:
        """Return as a key suitable for frontend use.

        See `build_str_key` static method for examples.
        """
        return self.build_str_key(
            self.cost_centre_id,
            self.natural_account_code_id,
            self.programme_id,
            self.analysis1_code_id,
            self.analysis2_code_id,
            self.project_code_id,
            **kwargs,
        )

    @staticmethod
    def build_str_key(
        cost_centre_code: str,
        nac: str,
        programme: str,
        analysis1: str | None = None,
        analysis2: str | None = None,
        project: str | None = None,
        year: str | int | None = None,
        period: str | int | None = None,
        separator="/",
    ) -> str:
        """Return a key suitable for frontend use.

        Mirrored by the javascript function `makeFinancialCodeKey`.

        Examples:
            With all arguments:
            "888812/71111001/338887/1234/5678/0001/2024/02"

            With minimal arguments:
            "888812/71111001/338887/////"
        """
        return separator.join(
            str(x) if x is not None else ""
            for x in [
                cost_centre_code,
                nac,
                programme,
                analysis1,
                analysis2,
                project,
                year,
                period,
            ]
        )

    def human_readable_format(self):
        cost_centre = (
            f"(Cost Centre: {self.cost_centre.cost_centre_code}"
            f"-{self.cost_centre.cost_centre_name})"
        )
        nac = (
            f"(NAC: {self.natural_account_code.natural_account_code}"
            f"-{self.natural_account_code.natural_account_code_description})"
        )
        programme = (
            f"(Programme: {self.programme.programme_code}"
            f"-{self.programme.programme_description})"
        )
        if self.project_code:
            project = (
                f"(Project: {self.project_code.project_code}"
                f"-{self.project_code.project_description})"
            )
        else:
            project = ""
        if self.analysis1_code:
            analysis1 = (
                f"(Contract: {self.analysis1_code.analysis1_code}"
                f"-{self.analysis1_code.analysis1_description})"
            )
        else:
            analysis1 = ""
        if self.analysis2_code:
            analysis2 = (
                f"(Market: {self.analysis2_code.analysis2_code}"
                f"-{self.analysis2_code.analysis2_description})"
            )
        else:
            analysis2 = ""
        return f"{cost_centre}{nac}{programme}{analysis1}{analysis2}{project}"

    def __str__(self):
        return self.human_readable_format()


class SubTotalForecast:
    result_table = []
    period_list = []
    full_list = []
    output_subtotal = []
    previous_values = []
    display_total_column = ""

    def __init__(self, data):
        self.display_data = data
        self.result_table = []
        self.period_list = []
        self.full_list = []
        self.output_subtotal = []
        self.previous_values = []
        self.display_total_column = ""

    def output_row_to_table(self, row, style_name=""):
        #     Add the stile entry to the dictionary
        #     add the resulting dictionary to the list
        # if style_name != '':
        #     style_name = '{}-{}'.format(style_name, level)
        row["row_type"] = style_name
        self.result_table.append(row)

    def add_row_to_subtotal(self, row_from, sub_total):
        for period in self.period_list:
            val = None
            if row_from[period]:
                val = row_from[period]
            else:
                val = 0
            if sub_total[period]:
                sub_total[period] += val
            else:
                sub_total[period] = val

    def clear_row(self, row):
        for period in self.period_list:
            row[period] = 0

    def row_has_values(self, row):
        has_values = False
        for period in self.period_list:
            if row[period] and (row[period] > 50 or row[period] < -50):
                has_values = True
                break
        return has_values

    def remove_empty_rows(self):
        # period_list has to be initialised before we can check if the row
        # has values different from 0
        how_many_row = len(self.display_data) - 1
        for i in range(how_many_row, -1, -1):
            row = self.display_data[i]
            if not self.row_has_values(row):
                del self.display_data[i]

    def do_output_subtotal(self, current_row):
        new_flag = False
        # Check the subtotals, from the outer subtotal to the inner one.
        # if an outer subtotal is needed, all the inner one are needed too
        for column in self.subtotal_columns[::-1]:
            if self.output_subtotal[column]:
                # this trigger the subtotals in the inner fields.
                new_flag = True
            else:
                self.output_subtotal[column] = new_flag

        for column in self.subtotal_columns:
            if self.output_subtotal[column]:
                subtotal_row = self.subtotals[column].copy()
                level = self.subtotal_columns.index(column)
                subtotal_row[self.display_total_column] = (
                    f"Total {self.previous_values[column]}"
                )
                show_class = TOTAL_CLASS
                for out_total in self.subtotal_columns[level + 1 :]:
                    subtotal_row[self.display_total_column] = (
                        f"{subtotal_row[self.display_total_column]} "
                        f"{self.previous_values[out_total]}"
                    )
                    show_class = SUB_TOTAL_CLASS
                self.output_row_to_table(
                    subtotal_row,
                    show_class,
                )
                self.clear_row(self.subtotals[column])
                self.previous_values[column] = current_row[column]
                self.output_subtotal[column] = False
            else:
                break

    def calculate_subtotal_data(
        self,
        display_total_column,
        subtotal_columns_arg,
        show_grand_total,
    ):
        # Make a copy so that modifying this will not touch
        # the original subtotal_columns_arg
        # otherwise each time the view is called the calculation order changes.
        self.subtotal_columns = copy.deepcopy(subtotal_columns_arg)
        # The self.subtotals are passed in from
        # the outer totals for calculation,
        # it is easier to call subtotal 0
        # the innermost subtotal
        self.subtotal_columns.reverse()
        self.display_total_column = display_total_column
        self.result_table = []
        self.output_subtotal = []
        self.previous_values = []

        self.full_list = list(
            FinancialPeriod.objects.values_list("period_short_name", flat=True)
        )

        self.full_list.append(budget_field)
        self.full_list.append("Previous_outturn")
        self.full_list.append(outturn_field)
        self.full_list.append(outturn_variance_field)

        # remove missing periods (like Adj1,
        # etc from the list used to add the
        # periods together.
        self.period_list = [
            value for value in self.full_list if value in self.display_data[0].keys()
        ]

        self.remove_empty_rows()
        # Check that there are rows left. Maybe they were all
        # with values of 0.
        if not self.display_data:
            return []
        first_row = self.display_data.pop(0)
        self.output_row_to_table(first_row, "")
        # Initialise the structure required
        # a dictionary with the previous
        # value of the columns to be
        # sub-totalled a dictionary of
        # subtotal dictionaries, with an
        # extra entry for the final total
        # (gran total)
        sub_total_row = {
            k: (v if k in self.period_list else " ") for k, v in first_row.items()
        }
        self.previous_values = {
            field_name: first_row[field_name] for field_name in self.subtotal_columns
        }
        # initialise all the self.subtotals,
        # and add an extra row for the
        # final total (gran total)
        self.subtotals = {
            field_name: sub_total_row.copy() for field_name in self.subtotal_columns
        }

        self.subtotals[GRAND_TOTAL_ROW] = sub_total_row.copy()
        self.output_subtotal = {
            field_name: False for field_name in self.subtotal_columns
        }
        for current_row in self.display_data:
            subtotal_time = False
            # check if we need a subtotal.
            # we check from the inner subtotal
            for column in self.subtotal_columns:
                if current_row[column] != self.previous_values[column]:
                    subtotal_time = True
                    self.output_subtotal[column] = True
            if subtotal_time:
                self.do_output_subtotal(current_row)
            for _, totals in self.subtotals.items():
                self.add_row_to_subtotal(current_row, totals)
            self.output_row_to_table(current_row, "")

        # output all the subtotals, because it is finished
        for column in self.subtotal_columns:
            level = self.subtotal_columns.index(column)
            caption = f"Total {self.previous_values[column]}"
            show_class = TOTAL_CLASS
            for out_total in self.subtotal_columns[level + 1 :]:
                caption = f"{caption} {self.previous_values[out_total]}"
                show_class = SUB_TOTAL_CLASS

            self.subtotals[column][self.display_total_column] = caption
            self.output_row_to_table(
                self.subtotals[column],
                show_class,
            )
        if show_grand_total:
            self.subtotals[GRAND_TOTAL_ROW][
                self.display_total_column
            ] = "Total Managed Expenditure"
            self.output_row_to_table(self.subtotals[GRAND_TOTAL_ROW], GRAND_TOTAL_CLASS)

        return self.result_table


class PivotManager(models.Manager):
    """Managers returning the data in Monthly figures pivoted"""

    def pivot_data(self, columns, filter_dict=None, year=0, order_list=None):
        if filter_dict is None:
            filter_dict = {}

        if order_list is None:
            order_list = []

        if year == 0:
            year = get_current_financial_year()

        q1 = (
            self.get_queryset()
            .filter(financial_year=year, **filter_dict)
            .order_by(*order_list)
        )
        pivot_data = pivot(
            q1,
            columns,
            "financial_period__period_short_name",
            "amount",
        )
        return pivot_data


class DisplaySubTotalManager(models.Manager):
    """Managers returning the actual/forecast/budget data
    in a format suitable for display"""

    def subtotal_data(
        self,
        display_total_column,
        subtotal_columns,
        data_columns,
        filter_dict=None,
        year=0,
        order_list=None,
        show_grand_total=True,
    ):
        if filter_dict is None:
            filter_dict = {}

        if order_list is None:
            order_list = []

        # If requesting a subtotal, the
        # list of columns must be specified
        if not subtotal_columns:
            raise SubTotalFieldNotSpecifiedError("Sub-total field not specified")

        correct = True
        error_msg = ""
        for elem in subtotal_columns:
            if elem not in [*data_columns]:
                correct = False
                error_msg += f"'{elem}', "
        if not correct:
            raise SubTotalFieldDoesNotExistError(
                f"Sub-total column(s) {error_msg} not found."
            )

        if display_total_column not in [*data_columns]:
            raise SubTotalFieldDoesNotExistError(
                f"Display sub-total column '{display_total_column}' "
                f"does not exist in provided columns: '{[*data_columns]}'."
            )

        data_returned = self.raw_data_annotated(
            data_columns, filter_dict, year, order_list
        )
        raw_data = list(data_returned)
        if not raw_data:
            return []
        r = SubTotalForecast(raw_data)
        return r.calculate_subtotal_data(
            display_total_column,
            subtotal_columns,
            show_grand_total,
        )

    def raw_data_annotated(self, columns, filter_dict=None, year=0, order_list=None):
        if filter_dict is None:
            filter_dict = {}

        if order_list is None:
            order_list = []

        annotations = {
            budget_field: Sum("budget"),
            "Apr": Sum("apr"),
            "May": Sum("may"),
            "Jun": Sum("jun"),
            "Jul": Sum("jul"),
            "Aug": Sum("aug"),
            "Sep": Sum("sep"),
            "Oct": Sum("oct"),
            "Nov": Sum("nov"),
            "Dec": Sum("dec"),
            "Jan": Sum("jan"),
            "Feb": Sum("feb"),
            "Mar": Sum("mar"),
            "Adj1": Sum("adj1"),
            "Adj2": Sum("adj2"),
            "Adj3": Sum("adj3"),
            outturn_field: Sum(
                F("apr")
                + F("may")
                + F("jun")
                + F("jul")
                + F("aug")
                + F("sep")
                + F("oct")
                + F("nov")
                + F("dec")
                + F("jan")
                + F("feb")
                + F("mar")
                + F("adj1")
                + F("adj2")
                + F("adj3")
            ),
            outturn_variance_field: Sum(
                F("apr")
                + F("may")
                + F("jun")
                + F("jul")
                + F("aug")
                + F("sep")
                + F("oct")
                + F("nov")
                + F("dec")
                + F("jan")
                + F("feb")
                + F("mar")
                + F("adj1")
                + F("adj2")
                + F("adj3")
                - F("previous_outturn")
            ),
            "Previous_outturn": Sum("previous_outturn"),
        }
        if year == 0:
            year = get_current_financial_year()
        year_filter = Q(financial_year=year)

        if self.model.__name__ == "ForecastingDataView":
            # The data changes only in the tables used by ForecastingDataView
            # so use it as indicator for caches
            dont_use_cache = True
        else:
            dont_use_cache = False

        if dont_use_cache:
            raw_data = (
                self.get_queryset()
                .values(*columns)
                .filter(
                    year_filter,
                    **filter_dict,
                )
                .annotate(**annotations)
                .order_by(*order_list)
            )
        else:
            # Get previous year from cache if possible
            query_key = f"{self.model._meta.db_table}_{str(columns)}_{str(filter_dict)}_{str(year)}"  # noqa
            key_slug = slugify(query_key)
            cache_key = hashlib.md5(str.encode(key_slug)).hexdigest()
            try:
                raw_data = cache.get(cache_key)

                if raw_data:
                    return raw_data
            except:  # noqa E722
                pass

            raw_data = (
                self.get_queryset()
                .values(*columns)
                .filter(
                    year_filter,
                    **filter_dict,
                )
                .annotate(**annotations)
                .order_by(*order_list)
            )
            # 7 day cache period
            cache_invalidation_time = 7 * 24 * 60 * 60
            try:
                cache.set(
                    cache_key,
                    raw_data,
                    cache_invalidation_time,
                )
            except:  # noqa E722
                pass

        return raw_data


# Does not inherit from BaseModel as it maps to database view
class ForecastingDataViewAbstract(models.Model):
    """Used for joining budgets and forecast.
    The view adds rows with 0 values across the year (zero-values rows),
    to be consistent with the Edit Forecast logic.
    The zero-values rows have a null value for the year,
    because the year is linked to the figures, and they have none!
    Mapped to a view in the database, because
    the query is too complex"""

    id = models.IntegerField(
        primary_key=True,
    )
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.DO_NOTHING,
    )
    financial_year = models.IntegerField()
    budget = models.BigIntegerField(default=0)
    apr = models.BigIntegerField(default=0)
    may = models.BigIntegerField(default=0)
    jun = models.BigIntegerField(default=0)
    jul = models.BigIntegerField(default=0)
    aug = models.BigIntegerField(default=0)
    sep = models.BigIntegerField(default=0)
    oct = models.BigIntegerField(default=0)
    nov = models.BigIntegerField(default=0)
    dec = models.BigIntegerField(default=0)
    jan = models.BigIntegerField(default=0)
    feb = models.BigIntegerField(default=0)
    mar = models.BigIntegerField(default=0)
    adj1 = models.BigIntegerField(default=0)
    adj2 = models.BigIntegerField(default=0)
    adj3 = models.BigIntegerField(default=0)
    previous_outturn = models.BigIntegerField(
        default=0,
        blank=True,
        null=True,
    )
    objects = models.Manager()  # The default manager.
    view_data = DisplaySubTotalManager()

    class Meta:
        abstract = True


class ForecastingDataView(ForecastingDataViewAbstract):
    # The view is created by a migration. Its code is at the bottom of this file.
    class Meta:
        managed = False
        db_table = "forecast_forecast_download_view"


class MonthlyFigureQuerySet(models.QuerySet):
    def forecast(self, financial_year: FinancialYear) -> Self:
        """Filter on the figure being a forecast based on the given financial year."""
        qs = self.filter(
            financial_year=financial_year,
            archived_status__isnull=True,
        )

        if financial_year.current:
            qs = self.filter(financial_period__actual_loaded=False)

        return qs


class MonthlyFigureAbstract(BaseModel):
    """It contains the forecast and the actuals.
    The current month defines what is Actual and what is Forecast"""

    id = models.AutoField(primary_key=True)

    amount = models.BigIntegerField(default=0)  # stored in pence
    financial_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.PROTECT,
    )
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    objects = MonthlyFigureQuerySet.as_manager()
    pivot = PivotManager()

    # TODO don't save to month that have actuals
    class Meta:
        abstract = True

    def __str__(self):
        return (
            f"{self.financial_code.cost_centre}"
            f"--{self.financial_code.programme}"
            f"--{self.financial_code.natural_account_code}"
            f"--{self.financial_code.analysis1_code}"
            f"--{self.financial_code.analysis2_code}"
            f"--{self.financial_code.project_code}:"
            f"{self.financial_year} "
            f"{self.financial_period} "
            f"{self.amount}"
        )


class ForecastMonthlyFigure(MonthlyFigureAbstract):
    starting_amount = models.BigIntegerField(default=0)
    # If archived_status is null, the record is the current one.
    # Because EndOfMonthStatus uses FinancialPeriod,
    #  it cannot be imported from the end_of_month models: it gives
    #  a circular reference and several errors.
    archived_status = models.ForeignKey(
        "end_of_month.EndOfMonthStatus",
        on_delete=models.PROTECT,
        related_name="forecast_forecastmonthlyfigures",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                    "archived_status",
                ],
                name="ForecastMonthlyFigure_unique1",
                condition=Q(archived_status__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                ],
                name="ForecastMonthlyFigure_unique2",
                condition=Q(archived_status__isnull=True),
            ),
        ]


class ActualUploadMonthlyFigure(MonthlyFigureAbstract):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                ],
                name="ActualUploadMonthlyFigure_unique1",
            ),
        ]


class BudgetMonthlyFigure(MonthlyFigureAbstract):
    """Used to store the budgets
    for the financial year."""

    starting_amount = models.BigIntegerField(default=0)
    # If archived_status is null, the record is the current one.
    # Because EndOfMonthStatus uses FinancialPeriod,
    #  it cannot be imported from the end_of_month models: it gives
    #  a circular reference and several errors.
    archived_status = models.ForeignKey(
        "end_of_month.EndOfMonthStatus",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                    "archived_status",
                ],
                name="BudgetMonthlyFigure_unique1",
                condition=Q(archived_status__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                ],
                name="BudgetMonthlyFigure_unique2",
                condition=Q(archived_status__isnull=True),
            ),
        ]


class BudgetUploadMonthlyFigure(MonthlyFigureAbstract):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "financial_code",
                    "financial_year",
                    "financial_period",
                ],
                name="BudgetUploadMonthlyFigure_unique1",
            ),
        ]
