from collections import OrderedDict

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

    def render(self, value):
        if f'{value}'.strip():
            return 'View'
        return ''


class ForecastFigureCol(tables.Column):
    # display 0 for null value instead of a dash
    default = 0
    tot_value = 0

    def display_value(self, value):
        return value

    def render(self, value):
        if type(value) == str:
            value = 0
        v = value or 0
        self.tot_value += v
        return self.display_value(v)

    def value(self, record, value):
        return float(value or 0)

    def __init__(self, show_footer, *args, **kwargs):
        self.show_footer = show_footer
        super().__init__(*args, **kwargs)
        if show_footer:
            self.render_footer = self.proto_render_footer

    def proto_render_footer(self, bound_column, table):
        return self.display_value(self.tot_value)


class SummingMonthFooterCol(ForecastFigureCol):
    """It expects a list of month as first argument.
    Used to calculate and display year to date, full year, etc"""
    def calc_value(self, record):
        val = sum(
            record[m] for m in self.month_list if m in record and record[m] is not None
        )
        return val or 0

    def render(self, value, record):
        val = self.calc_value(record)
        self.tot_value += val
        return self.display_value(val)

    def value(self, record, value):
        val = self.calc_value(record)
        return float(val)

    def __init__(self, month_list, *args, **kwargs):
        self.month_list = month_list
        super().__init__(*args, **kwargs)


class SubtractCol(ForecastFigureCol):
    """Used to display the difference between the figures in two columns"""

    def calc_value(self, table):
        a = table.columns.columns[self.col1].current_value
        b = table.columns.columns[self.col2].current_value
        val = a - b
        return self.display_value(val)

    def render(self, table):
        return self.calc_value(table)

    def value(self, table):
        return self.calc_value(table)

    def __init__(self, col1, col2, *args, **kwargs):
        self.col1 = col1
        self.col2 = col2
        super().__init__(*args, **kwargs)


class PercentageCol(ForecastFigureCol):
    """Used to display the percentage of values in two columns"""
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


class ForecastTable(tables.Table):
    """Define the month columns format and their footer.
    Used every time we need to display a forecast"""
    display_footer = True
    display_view_details = False

    def __init__(self, column_dict={}, *args, **kwargs):
        cols = [
            ("Budget",
             ForecastFigureCol(self.display_footer, budget_header, empty_values=()))
        ]
        # Only add the month columns here. If you add the adjustments too,
        # their columns will be displayed even after 'display_figure' field is False
        for month in FinancialPeriod.financial_period_info.month_display_list():
            cols.append(
                (
                    month,
                    ForecastFigureCol(self.display_footer, month, empty_values=()),
                )
            )

        self.base_columns.update(OrderedDict(cols))

        # Remove the columns with a
        # value of 'Hidden'. They are
        # needed in the dataset for
        #  calculating the subtotals,
        #  but they are not required
        #  in the displayed table.
        column_dict = {k: v for k, v in column_dict.items() if v != "Hidden"}

        extra_column_to_display = [
            (k, tables.Column(v)) for (k, v) in column_dict.items()
        ]
        column_list = list(column_dict.keys())
        if self.display_view_details:
            extra_column_to_display.extend(
                [("Link",
                  self.link_col,
                  )]
            )
            column_list.insert(0, "Link")

        actual_month_list = FinancialPeriod.financial_period_info.actual_month_list()
        # See if Adjustment periods should be displayed.
        # Add them as extra columns, otherwise they remain visible even after
        # their field 'display_figure' is set to False.
        adj_list = FinancialPeriod.financial_period_info.adj_display_list()
        if adj_list:
            for adj in adj_list:
                extra_column_to_display.extend(
                    [(
                        adj,
                        ForecastFigureCol(self.display_footer, adj, empty_values=()),
                    )]
                )

        extra_column_to_display.extend(
            [
               (
                    "year_total",
                    SummingMonthFooterCol(
                        FinancialPeriod.financial_period_info.period_display_list(),
                        self.display_footer,
                        forecast_total_header,
                        empty_values=(),
                    ),
                ),
                (
                    "spend",
                    SubtractCol(
                        "Budget",
                        "year_total",
                        self.display_footer,
                        variance_header,
                        empty_values=(),
                    ),
                ),
                (
                    "percentage",
                    PercentageCol(
                        "spend",
                        "Budget",
                        self.display_footer,
                        variance_percentage_header,
                        empty_values=()
                    ),
                ),
                (
                    "year_to_date",
                    SummingMonthFooterCol(
                        actual_month_list,
                        self.display_footer,
                        year_to_date_header,
                        empty_values=(),
                    ),
                ),
                (
                "percentage_spent",
                PercentageCol(
                    "year_to_date",
                    "Budget",
                    self.display_footer,
                    budget_spent_percentage_header,
                    empty_values=()
                ),
               ),
            ]
        )

        super().__init__(
            extra_columns=extra_column_to_display,
            sequence=column_list, *args, **kwargs,
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
            "class": "govuk-table",
            "thead": {"class": "govuk-table__head"},
            "tbody": {"class": "govuk-table__body"},
            "th": {"class": "govuk-table__header"},
            "td": {"class": "govuk-table__cell"},
            "tf": {"class": "govuk-table__cell"},
            "a": {"class": "govuk-link"},
        }
        orderable = False
        row_attrs = {"class": "govuk-table__row"}


class ForecastSubTotalTable(ForecastTable, tables.Table):
    display_footer = False

    class Meta(ForecastTable.Meta):
        row_attrs = {
            "class": lambda record: "govuk-table__row {}".format(record["row_type"])
        }


class ForecastWithLinkTable(ForecastSubTotalTable, tables.Table):
    display_view_details = True

    def __init__(self, viewname, arg_link, code='', *args, **kwargs):

        link_args = []
        if code:
            link_args.append(code)

        for item in arg_link:
            link_args.append(tables.A(item))

        self.link_col = ForecastLinkCol(
            '',
            arg_link[0],
            attrs={
                "class": "govuk-link"
            },
            linkify={
                "viewname": viewname,
                "args": link_args,
            }
        )

        super().__init__(*args, **kwargs)

    class Meta(ForecastSubTotalTable.Meta):
        pass
