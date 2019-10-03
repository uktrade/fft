from collections import OrderedDict

from django.contrib.humanize.templatetags.humanize import intcomma


import django_tables2 as tables

from .models import FinancialPeriod


class SummingFooterCol(tables.Column):
    # display 0 for null value instead of a dash
    default = 0
    tot_value = 0

    def render(self, value):
        v = (value or 0)
        self.tot_value += v
        # return '{:0.2f}'.format(value)
        return intcomma(v)

    def value(self, record, value):
        return float(value or 0)

    def __init__(self, show_footer, *args, **kwargs):
        self.show_footer = show_footer
        super().__init__(*args, **kwargs)
        if show_footer:
            self.render_footer = self.proto_render_footer

    def proto_render_footer(self, bound_column, table):
        return intcomma(self.tot_value)


class SummingMonthFooterCol(SummingFooterCol):
    """It expects a list of month as first argument.
    Used to calculate and display year to date, full year, etc"""

    def calc_value(self, record):
        val = sum(record[m] for m in self.month_list if record[m] is not None)
        return val or 0

    def render(self, value, record):
        val = self.calc_value(record)
        self.tot_value += val
        return intcomma(val)

    def value(self, record, value):
        val = self.calc_value(record)
        return float(val)

    def __init__(self, month_list, *args, **kwargs):
        self.month_list = month_list
        super().__init__(*args, **kwargs)


class ForecastTable(tables.Table):
    """Define the month columns format and their footer.
    Used every time we need to display a forecast"""
    display_footer = True

    def __init__(self, column_dict={}, *args, **kwargs):
        cols = [(
            'budg',
            SummingFooterCol(self.display_footer, 'Budget', empty_values=())
        )]

        for month in FinancialPeriod.financial_period_info.periods():
            cols.append((
                month[0],
                SummingFooterCol(self.display_footer, month[1], empty_values=())
            ))

        self.base_columns.update(OrderedDict(cols))

        # Remove the columns with a value of 'Hidden'. They are needed in the dataset for
        #  calculating the subtotals, but they are not required in the displayed table.
        column_dict = {k: v for k, v in column_dict.items() if v != 'Hidden'}
        extra_column_to_display = [(k, tables.Column(v)) for (k, v) in column_dict.items()]

        column_list = column_dict.keys()
        actual_month_list = FinancialPeriod.financial_period_info.actual_month_list()

        extra_column_to_display.extend(
            [
                (
                    'year_to_date',
                    SummingMonthFooterCol(
                        actual_month_list,
                        self.display_footer,
                        'Year to Date',
                        empty_values=()
                    )
                ),
                (
                    'year_total',
                    SummingMonthFooterCol(
                        FinancialPeriod.financial_period_info.period_display_list(),
                        self.display_footer,
                        'Year Total',
                        empty_values=()
                    )
                )
            ]
        )

        super().__init__(
            extra_columns=extra_column_to_display,
            sequence=column_list, *args, **kwargs
        )
        # change the stile for columns showing actuals. It has to be done after super().__init__
        # otherwise it gets overwritten.
        for month in actual_month_list:
            col = self.columns[month]
            col.column.attrs = {
                'td': {'class': 'actual-month'}
            }

    class Meta:
        template_name = 'django_tables_2_bootstrap.html'
        empty_text = ''
        attrs = {
            "class": "govuk-table",
            "caption": "Financial Report",
            "thead": {'class': 'govuk-table__head'},
            "tbody": {'class': 'govuk-table__body'},
            'th': {'class': 'govuk-table__header'},
            'td': {'class': 'govuk-table__cell'},
            'tf': {'class': 'govuk-table__cell'}
        }
        orderable = False
        row_attrs = {
            "class": "govuk-table__row"
        }


class ForecastSubTotalTable(ForecastTable, tables.Table):
    display_footer = False

    class Meta(ForecastTable.Meta):
        row_attrs = {
            "class": lambda record: 'govuk-table__row {}'.format(record["row_type"]),
        }
