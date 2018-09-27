from django.contrib.humanize.templatetags.humanize import intcomma

import django_tables2 as tables


class ColumnWithThousandsSeparator(tables.Column):
    def render(self, value):
        return intcomma(value)

    attrs = {'td': {'class': 'text-right'},
             'th': {'class': 'text-right'},
             'tf': {'class': 'text-right font-weight-bold'}}


class SummingColumn(ColumnWithThousandsSeparator):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class ADIReportTable(tables.Table):
    cost_centre__directorate__group__group_name = tables.Column('Departmental Group')

    apr__sum = SummingColumn('April')
    may__sum = SummingColumn('May')
    jun__sum = SummingColumn('June')
    jul__sum = SummingColumn('July')
    aug__sum = SummingColumn('August')
    sep__sum = SummingColumn('September')
    oct__sum = SummingColumn('October')
    nov__sum = SummingColumn('November')
    dec__sum = SummingColumn('December')
    jan__sum = SummingColumn('January')
    feb__sum = SummingColumn('February')
    mar__sum = SummingColumn('March')

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table-striped table-bordered table-condensed small-font"}
        empty_text = ""
