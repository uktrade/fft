from collections import OrderedDict

from django.urls import reverse
from django.utils.html import format_html

import django_tables2 as tables

from forecast.models import FinancialPeriod
from forecast.utils.view_header_definition import (
    budget_header,
    budget_spent_percentage_header,
    forecast_total_header,
    variance_header,
    variance_percentage_header,
    year_to_date_header,
)


class ForecastLinkCol(tables.Column):
    # Because of the subtotals in the columns, it is not possible to use linkify
    # So the html is generated here.
    # If the row_type has a value, the row is a total row, so don't create the link
    def render(self, value, record):
        if record['row_type'] != '':
            return value
        else:
            args = [record.get(v, v) for v in self.link_args]
            url = reverse(self.viewname, args=args)
            return format_html('<a href="{}">{}</a>', url, value)


class SummingMonthCol(tables.Column):
    """It expects a list of month as first argument.
    Used to calculate and display year to date, full year, etc"""

    def calc_value(self, record):
        val = sum(
            record[m] for m in self.month_list if m in record and record[m] is not None
        )
        return val or 0

    def display_value(self, value):
        return value

    def render(self, value, record):
        val = self.calc_value(record)
        return self.display_value(val)

    def value(self, record, value):
        val = self.calc_value(record)
        return float(val)

    def __init__(self, month_list, *args, **kwargs):
        self.month_list = month_list
        super().__init__(*args, **kwargs)


class SubtractCol(tables.Column):
    """Used to display the difference between the figures in two columns"""

    def calc_value(self, table):
        a = table.columns.columns[self.col1].current_value
        b = table.columns.columns[self.col2].current_value
        val = a - b
        return self.display_value(val)

    def display_value(self, value):
        return value

    def render(self, table):
        return self.calc_value(table)

    def value(self, table):
        return self.calc_value(table)

    def __init__(self, col1, col2, *args, **kwargs):
        self.col1 = col1
        self.col2 = col2
        super().__init__(*args, **kwargs)


class PercentageCol(tables.Column):
    """Used to display the percentage of values in two columns"""
    attrs = {
        "td": {"class": "govuk-table__cell  govuk-table__cell--numeric"},
    }

    def display_value(self, value):
        return f"{value:.0%}"

    def calc_value(self, table):
        a = table.columns.columns[self.col1].current_value
        b = table.columns.columns[self.col2].current_value
        if b == 0:
            return "No Budget"
        val = a / b
        return self.display_value(val)

    def render(self, table):
        return self.calc_value(table)

    def value(self, table):
        return self.calc_value(table)

    def __init__(self, col1, col2, *args, **kwargs):
        self.col1 = col1
        self.col2 = col2
        super().__init__(*args, **kwargs)


class ForecastSubTotalTable(tables.Table):
    """Define the month columns format.
    Used every time we need to display a forecast"""
    display_view_details = False

    def __init__(self, column_dict={}, *args, **kwargs):
        cols = [
            ("Budget",
             tables.Column(budget_header, empty_values=()))
        ]
        year_period_list = []
        # Only add the month columns here. If you add the adjustments too,
        # their columns will always be displayed
        for month in FinancialPeriod.financial_period_info.month_display_list():
            cols.append((month, tables.Column(month, empty_values=()),))
            year_period_list.append(month)

        self.base_columns.update(OrderedDict(cols))

        # Remove the columns with a
        # value of 'Hidden'. They are
        # needed in the dataset for
        #  calculating the subtotals,
        #  but they are not required
        #  in the displayed table.
        column_dict = {k: v for k, v in column_dict.items() if v != "Hidden"}
        column_list = list(column_dict.keys())
        self.num_meta_cols = len(column_list)

        if self.display_view_details:
            extra_column_to_display = [
                (k, tables.Column(v)) for (k, v) in column_dict.items() if
                k != self.column_name
            ]
            extra_column_to_display.extend([(self.column_name, self.link_col,)])
        else:
            extra_column_to_display = [(k, tables.Column(v)) for (k, v) in
                                       column_dict.items()]

        actual_month_list = kwargs.pop('actual_month_list', [])
        self.num_actuals = len(actual_month_list)

        # See if Adjustment periods should be displayed.
        # Add them as extra columns, otherwise they remain visible even after
        # their field 'display_figure' is set to False.
        # The list is passed as an argument, because it is different for previous years
        adj_list = kwargs.pop('adj_visible_list', [])
        if adj_list:
            for adj in adj_list:
                year_period_list.append(adj)
                extra_column_to_display.extend(
                    [(
                        adj,
                        tables.Column(adj, empty_values=()),
                    )]
                )

        extra_column_to_display.extend(
            [
                (
                    "year_total",
                    SummingMonthCol(
                        year_period_list,
                        forecast_total_header,
                        empty_values=(),
                    ),
                ),
                (
                    "spend",
                    SubtractCol(
                        "Budget",
                        "year_total",
                        variance_header,
                        empty_values=(),
                    ),
                ),
                (
                    "percentage",
                    PercentageCol(
                        "spend",
                        "Budget",
                        variance_percentage_header,
                        empty_values=()
                    ),
                ),
                (
                    "year_to_date",
                    SummingMonthCol(
                        actual_month_list,
                        year_to_date_header,
                        empty_values=(),
                    ),
                ),
                (
                    "percentage_spent",
                    PercentageCol(
                        "year_to_date",
                        "Budget",
                        budget_spent_percentage_header,
                        empty_values=()
                    ),
                ),
            ]
        )

        self.forecast_cols = (12 + len(extra_column_to_display)) - self.num_actuals

        super().__init__(
            extra_columns=extra_column_to_display,
            sequence=column_list,
            *args,
            **kwargs,
        )
        # change the stile for columns showing "actuals".
        # It has to be done after super().__init__
        # otherwise it gets overwritten.
        for month in actual_month_list:
            col = self.columns[month]
            col.column.attrs = {"td": {"class": "govuk-table__cell actual-month"}}

    class Meta:
        template_name = "django_tables_2_bootstrap.html"
        empty_text = ""
        attrs = {
            "class": "govuk-table finance-table",
            "thead": {"class": "govuk-table__head"},
            "tbody": {"class": "govuk-table__body"},
            "th": {"class": "govuk-table__header"},
            "td": {"class": "govuk-table__cell"},
            "tf": {"class": "govuk-table__cell"},
            "a": {"class": "govuk-link"},
        }
        orderable = False
        row_attrs = {
            "class": lambda record: "govuk-table__row {}".format(record["row_type"]),
        }


class ForecastWithLinkTable(ForecastSubTotalTable, tables.Table):
    display_view_details = True

    def __init__(self, column_name, viewname, arg_link, code="", column_dict={},
                 *args,
                 **kwargs):

        link_args = []
        if code:
            link_args.append(code)
        # Save the name of the columns, so we can find it when
        # processing the columns in ForecastSubTotalTable
        self.column_name = column_name
        # Find the column to be linked
        for item in arg_link:
            link_args.append(tables.A(item))

        self.link_col = ForecastLinkCol(
            column_dict.get(column_name),
            column_name,
            attrs={"class": "govuk-link"},
        )
        self.link_col.viewname = viewname
        self.link_col.link_args = link_args
        self.heading = ""

        super().__init__(column_dict, *args, **kwargs)

    class Meta(ForecastSubTotalTable.Meta):
        pass
