from django.db import models
from django.db.models import (
    Max,
    Q,
    Sum,
    UniqueConstraint,
)

# https://github.com/martsberger/django-pivot/blob/master/django_pivot/pivot.py # noqa
from django_pivot.pivot import pivot

from simple_history.models import HistoricalRecords

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.metamodels import (
    SimpleTimeStampedModel,
)
from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.utils import GRAND_TOTAL_CLASS, SUB_TOTAL_CLASS

from costcentre.models import CostCentre

from forecast.utils.query_fields import DEFAULT_PIVOT_COLUMNS

GRAND_TOTAL_ROW = "grand_total"


class SubTotalFieldDoesNotExistError(Exception):
    pass


class SubTotalFieldNotSpecifiedError(Exception):
    pass


class ForecastEditLock(models.Model):
    locked = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return 'Forecast edit lock'

    class Meta:
        permissions = [
            ("can_set_edit_lock", "Can set edit lock"),
            ("can_edit_whilst_locked", "Can edit forecasts whilst locked"),
        ]


class ForecastExpenditureType(models.Model):
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


class FinancialPeriodManager(models.Manager):
    def period_display_list(self):
        return list(
            self.get_queryset()
                .filter(display_figure=True)
                .values_list("period_short_name", flat=True)
        )

    def actual_period_code_list(self):
        return list(
            self.get_queryset().filter(
                actual_loaded=True
            ).values_list(
                "financial_period_code",
                flat=True,
            )
        )

    def actual_month(self):
        m = (
            self.get_queryset()
                .filter(actual_loaded=True)
                .aggregate(Max("financial_period_code"))
        )
        return m["financial_period_code__max"] or 0

    def actual_month_list(self):
        return self.period_display_list()[: self.actual_month()]

    def periods(self):
        return (
            self.get_queryset()
                .filter(display_figure=True)
                .values_list("period_short_name", "period_long_name")
        )

    def reset_actuals(self):
        self.get_queryset().filter(
            actual_loaded=True,
        ).update(
            actual_loaded=False,
        )


class FinancialPeriod(models.Model):
    """Financial periods: correspond
    to month, but there are 3 extra
    periods at the end"""

    financial_period_code = models.IntegerField(primary_key=True)  # April = 1
    period_long_name = models.CharField(max_length=20)
    period_short_name = models.CharField(max_length=10)
    period_calendar_code = models.IntegerField()  # January = 1
    # use a flag to indicate if the "actuals"
    # have been uploaded instead of relying on the date
    # the "actuals" are manually uploaded, so it is not
    # guaranteed on which date they are uploaded
    actual_loaded = models.BooleanField(default=False)
    display_figure = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.
    financial_period_info = FinancialPeriodManager()

    class Meta:
        ordering = ["financial_period_code"]

    def __str__(self):
        return self.period_long_name


class FinancialCode(models.Model):
    """Contains the members of Chart of Account needed to create a unique key"""

    class Meta:
        # Several constraints required, to cover all the permutations of
        # fields that can be Null
        constraints = [
            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis1_code",
                        "analysis2_code",
                        "project_code",
                        ],
                name="financial_row_unique_6",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=False)
            ),
            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis2_code",
                        "project_code",
                        ],
                name="financial_row_unique_5a",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=False)
            ),

            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis1_code",
                        "project_code",
                        ],
                name="financial_row_unique_5b",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=False)
            ),

            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis1_code",
                        "analysis2_code",
                        ],
                name="financial_row_unique_5c",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=True)
            ),

            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "project_code",
                        ],
                name="financial_row_unique_4a",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=False)
            ),

            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis1_code",
                        ],
                name="financial_row_unique_4b",
                condition=Q(analysis1_code__isnull=False)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=True)
            ),
            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        "analysis2_code",
                        ],
                name="financial_row_unique_4c",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=False)
                & Q(project_code__isnull=True)
            ),

            UniqueConstraint(
                fields=["programme",
                        "cost_centre",
                        "natural_account_code",
                        ],
                name="financial_row_unique_3",
                condition=Q(analysis1_code__isnull=True)
                & Q(analysis2_code__isnull=True)
                & Q(project_code__isnull=True)
            ),
        ]
        permissions = [
            ("can_view_forecasts", "Can view forecast"),
            ("can_upload_files", "Can upload files"),
        ]

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
        null=True
    )
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Override save to calculate the forecast_expenditure_type.
        if self.pk is None:
            # calculate the forecast_expenditure_type
            nac_economic_budget_code = (
                self.natural_account_code.economic_budget_code
            )
            programme_budget_type = self.programme.budget_type_fk

            forecast_type = ForecastExpenditureType.objects.filter(
                programme_budget_type=programme_budget_type,
                nac_economic_budget_code=nac_economic_budget_code,
            )

            self.forecast_expenditure_type = forecast_type.first()

        super(FinancialCode, self).save(*args, **kwargs)


class SubTotalForecast:
    result_table = []
    period_list = []
    full_list = []
    output_subtotal = []
    previous_values = []
    display_total_column = ''

    def __init__(self, data):
        self.display_data = data

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
                print(f'Deleted {i}')
                del (self.display_data[i])

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
                subtotal_row[self.display_total_column] = \
                    f"Total {self.previous_values[column]}"

                for out_total in self.subtotal_columns[level + 1:]:
                    subtotal_row[self.display_total_column] = \
                        f"{subtotal_row[self.display_total_column]} " \
                        f"{self.previous_values[out_total]}"
                self.output_row_to_table(
                    subtotal_row,
                    SUB_TOTAL_CLASS,
                )
                self.clear_row(self.subtotals[column])
                self.previous_values[column] = current_row[column]
                self.output_subtotal[column] = False
            else:
                break

    def subtotal_data(
            self,
            display_total_column,
            subtotal_columns_arg,
            show_grand_total,
    ):
        # The self.subtotals are passed in from
        # the outer totals for calculation,
        # it is easier to call subtotal 0
        # the innermost subtotal
        self.subtotal_columns = subtotal_columns_arg
        self.subtotal_columns.reverse()
        self.display_total_column = display_total_column
        self.result_table = []
        self.output_subtotal = []
        self.previous_values = []

        self.full_list = list(
            FinancialPeriod.objects.values_list("period_short_name", flat=True)
        )

        # remove missing periods (like Adj1,
        # etc from the list used to add the
        # periods together.
        self.period_list = [
            value for value in self.full_list if value in self.display_data[0].keys()
        ]
        self.period_list.append('Budget')
        self.remove_empty_rows()
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
            for k, totals in self.subtotals.items():
                self.add_row_to_subtotal(current_row, totals)
            self.output_row_to_table(current_row, "")

        # output all the subtotals, because it is finished
        for column in self.subtotal_columns:
            level = self.subtotal_columns.index(column)
            caption = f"Total {self.previous_values[column]}"
            for out_total in self.subtotal_columns[level + 1:]:
                caption = f"{caption} {self.previous_values[out_total]}"
            self.subtotals[column][self.display_total_column] = caption
            self.output_row_to_table(
                self.subtotals[column],
                SUB_TOTAL_CLASS,
            )
        if show_grand_total:
            self.subtotals[GRAND_TOTAL_ROW][self.display_total_column] = \
                "Total Managed Expenditure"
            self.output_row_to_table(
                self.subtotals[GRAND_TOTAL_ROW], GRAND_TOTAL_CLASS
            )

        return self.result_table


class PivotManager(models.Manager):
    """Managers returning the data in Monthly figures pivoted"""
    default_columns = DEFAULT_PIVOT_COLUMNS

    def pivot_data(self, columns={}, filter_dict={}, year=0, order_list=[]):
        if year == 0:
            year = get_current_financial_year()
        if columns == {}:
            columns = self.default_columns

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
        # print(pivot_data.query)
        return pivot_data


class DisplaySubTotalManager(models.Manager):
    """Managers returning the actual/forecast/budget data
    in a format suitable for display"""

    default_columns = DEFAULT_PIVOT_COLUMNS

    def subtotal_data(
            self,
            display_total_column,
            subtotal_columns,
            data_columns,
            filter_dict={},
            year=0,
            order_list=[],
            show_grand_total=True
    ):
        # If requesting a subtotal, the
        # list of columns must be specified
        if not subtotal_columns:
            raise SubTotalFieldNotSpecifiedError("Sub-total field not specified")

        correct = True
        error_msg = ''
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

        data_returned = self.raw_data(data_columns, filter_dict, year, order_list)
        raw_data = list(data_returned)
        if not raw_data:
            return []
        r = SubTotalForecast(raw_data)
        return r.subtotal_data(
            display_total_column,
            subtotal_columns,
            show_grand_total,
        )

    def raw_data(self, columns={}, filter_dict={}, year=0, order_list=[]):
        if year == 0:
            year = get_current_financial_year()
        if columns == {}:
            columns = self.default_columns

        annotations = {'Budget': Sum('budget'),
                       'Apr': Sum('apr'),
                       'May': Sum('may'),
                       'Jun': Sum('jun'),
                       'Jul': Sum('jul'),
                       'Aug': Sum('aug'),
                       'Sep': Sum('sep'),
                       'Oct': Sum('oct'),
                       'Nov': Sum('nov'),
                       'Dec': Sum('dec'),
                       'Jan': Sum('jan'),
                       'Feb': Sum('feb'),
                       'Mar': Sum('mar'),
                       }
        raw_data = (self.get_queryset().values(*columns)
                    .filter(financial_year=year, **filter_dict)
                    .annotate(**annotations)
                    .order_by(*order_list)
                    )
        return raw_data


class ForecastBudgetDataView(models.Model):
    """Used for joining budgets and forecast.
    Mapped to a view in the database, because
    the query is too complex"""
    id = models.IntegerField(primary_key=True, )
    # The view is created by a migration. Its code is at the bottom of this file.
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
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
    objects = models.Manager()  # The default manager.
    sub_total = DisplaySubTotalManager()

    class Meta:
        managed = False
        db_table = "forecast_forecast_budget_view"


class MonthlyFigureAbstract(SimpleTimeStampedModel):
    """It contains the forecast and the actuals.
    The current month defines what is Actual and what is Forecast"""
    amount = models.BigIntegerField(default=0)  # stored in pence
    id = models.AutoField(primary_key=True)
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
    objects = models.Manager()  # The default manager.
    pivot = PivotManager()

    # TODO don't save to month that have actuals
    class Meta:
        abstract = True
        unique_together = (
            "financial_code",
            "financial_year",
            "financial_period",
        )

    def __str__(self):
        return f"{self.financial_code.cost_centre}" \
               f"--{self.financial_code.programme}" \
               f"--{self.financial_code.natural_account_code}" \
               f"--{self.financial_code.analysis1_code}" \
               f"--{self.financial_code.analysis2_code}" \
               f"--{self.financial_code.project_code}:" \
               f"{self.financial_year} " \
               f"{self.financial_period} " \
               f"{self.amount}"


class ForecastMonthlyFigure(MonthlyFigureAbstract):
    history = HistoricalRecords()
    starting_amount = models.BigIntegerField(default=0)


class ArchivedForecastMonthlyFigure(MonthlyFigureAbstract):
    is_actual = models.BooleanField(default=False)
    forecast_month = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name='historical_forecast_monthly_figures'
    )
    forecast_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.PROTECT,
        related_name='historical_forecast_monthly_figures'
    )


class ActualUploadMonthlyFigure(MonthlyFigureAbstract):
    pass


class BudgetMonthlyFigure(MonthlyFigureAbstract):
    """Used to store the budgets
    for the financial year."""
    history = HistoricalRecords()
    starting_amount = models.BigIntegerField(default=0)


class BudgetUploadMonthlyFigure(MonthlyFigureAbstract):
    pass


class OSCARReturn(models.Model):
    """Used for downloading the Oscar return.
    Mapped to a view in the database, because
    the query is too complex"""

    # The view is created by  migration 0038_auto_create_view_forecast_oscar_return.py
    row_number = models.BigIntegerField()
    # The Treasury Level 5 account returned by the query is the result of a coalesce.
    # It is easier to use it as a foreign key in django
    # for getting the account description
    # than doing another join in the query.
    account_l5_code = models.ForeignKey(
        "treasuryCOA.L5Account",
        on_delete=models.PROTECT,
        db_column="account_l5_code",
    )
    sub_segment_code = models.CharField(max_length=8, primary_key=True)
    sub_segment_long_name = models.CharField(max_length=255)
    # Treasury requires the returns in 1000. The query perform the required
    #  division and rounding.
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

    class Meta:
        managed = False
        db_table = "forecast_oscarreturn"
        ordering = ["sub_segment_code"]


"""
            DROP VIEW if exists forecast_forecast_budget_view ;
            DROP VIEW if exists yearly_budget;
            DROP VIEW if exists annual_forecast;
            
            CREATE VIEW annual_forecast as
                SELECT financial_code_id, financial_year_id,
                       SUM(CASE WHEN financial_period_id = 1 THEN amount ELSE NULL END) AS apr,
                       SUM(CASE WHEN financial_period_id = 2 THEN amount ELSE NULL END) AS may,
                       SUM(CASE WHEN financial_period_id = 3 THEN amount ELSE NULL END) AS jun,
                       SUM(CASE WHEN financial_period_id = 4 THEN amount ELSE NULL END) AS jul,
                       SUM(CASE WHEN financial_period_id = 5 THEN amount ELSE NULL END) AS aug,
                       SUM(CASE WHEN financial_period_id = 6 THEN amount ELSE NULL END) AS sep,
                       SUM(CASE WHEN financial_period_id = 7 THEN amount ELSE NULL END) AS oct,
                       SUM(CASE WHEN financial_period_id = 8 THEN amount ELSE NULL END) AS nov,
                       SUM(CASE WHEN financial_period_id = 9 THEN amount ELSE NULL END) AS "dec",
                       SUM(CASE WHEN financial_period_id = 10 THEN amount ELSE NULL END) AS jan,
                       SUM(CASE WHEN financial_period_id = 11 THEN amount ELSE NULL END) AS feb,
                       SUM(CASE WHEN financial_period_id = 12 THEN amount ELSE NULL END) AS mar,
                       SUM(CASE WHEN financial_period_id = 13 THEN amount ELSE NULL END) AS adj1 ,
                       SUM(CASE WHEN financial_period_id = 14 THEN amount ELSE NULL END) AS adj2 ,
                       SUM(CASE WHEN financial_period_id = 15 THEN amount ELSE NULL END) AS adj3
                FROM forecast_forecastmonthlyfigure
                GROUP BY financial_code_id,  financial_year_id;
                       
            CREATE VIEW yearly_budget as
                SELECT financial_code_id, financial_year_id, SUM(amount) AS budget
                FROM forecast_budgetmonthlyfigure
                GROUP BY financial_code_id, financial_year_id;
                      
            CREATE VIEW public.forecast_forecast_budget_view
            as
            SELECT coalesce(b.financial_code_id, f.financial_code_id) as financial_code_id,
                    coalesce(b.financial_year_id, f.financial_year_id) as financial_year,
                    coalesce(budget, 0) as budget,
                    coalesce(apr, 0) as apr,
                    coalesce(may, 0) as may,
                    coalesce(jun, 0) as jun,
                    coalesce(jul, 0) as jul,
                    coalesce(aug, 0) as aug,
                    coalesce(sep, 0) as sep,
                    coalesce(oct, 0) as oct,
                    coalesce(nov, 0) as nov,
                    coalesce("dec", 0) as "dec",
                    coalesce(jan, 0) as jan,
                    coalesce(feb, 0) as feb,
                    coalesce(mar, 0) as mar,
                    coalesce(adj1, 0) as adj1,
                    coalesce(adj2, 0) as adj2,
                    coalesce(adj3, 0) as adj3
            FROM annual_forecast f 
                FULL OUTER JOIN yearly_budget b
                    on b.financial_code_id = f.financial_code_id and b.financial_year_id = f.financial_year_id;                    


""" # noqa

"""
Query created in the database to return the info for the OSCAR return
DROP VIEW  if exists "forecast_oscarreturn";
CREATE VIEW "forecast_oscarreturn" as 
        SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
            coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id")
            account_l5_code,
            "treasurySS_subsegment"."sub_segment_code" ,
            "treasurySS_subsegment"."sub_segment_long_name" ,                    
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 1 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "apr",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 2 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "may",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 3 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jun",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 4 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jul",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 5 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "aug",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 6 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "sep",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 7 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "oct",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 8 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "nov",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 9 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "dec",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 10 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jan",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 11 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "feb",
            coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 12 THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "mar"
        FROM "forecast_monthlyfigureamount"
                INNER JOIN
                 "forecast_monthlyfigure" on (forecast_monthlyfigureamount.monthly_figure_id = forecast_monthlyfigure.id)
                INNER JOIN "forecast_financialcode" on (forecast_monthlyfigure.financial_code_id = forecast_financialcode.id)
                    LEFT OUTER JOIN "chartofaccountDIT_naturalcode"
                    ON ("forecast_financialcode"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code")
                    INNER JOIN "costcentre_costcentre"
                    ON ("forecast_financialcode"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code")
                    INNER JOIN "costcentre_directorate"
                    ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code")
                    INNER JOIN "costcentre_departmentalgroup"
                    ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code")
                    INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_financialcode"."programme_id" = "chartofaccountDIT_programmecode"."programme_code")
                        INNER JOIN "forecast_financialperiod" ON ("forecast_monthlyfigure"."financial_period_id" = "forecast_financialperiod"."financial_period_code")
                    LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
                    AND "chartofaccountDIT_programmecode"."budget_type_fk_id" = "treasurySS_subsegment"."dit_budget_type_id")
                    INNER JOIN "core_financialyear" ON ("forecast_monthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
                    WHERE "core_financialyear"."current" = TRUE and forecast_monthlyfigureamount.version = 1
                    GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
                    "treasurySS_subsegment"."sub_segment_code" ;        """  # noqa
