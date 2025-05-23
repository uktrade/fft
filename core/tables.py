import django_tables2 as tables


# Taken from https://owasp.org/www-community/attacks/CSV_Injection.
CSV_INJECTION_CHARS = ("=", "+", "-", "@", "\t", "\r")


def _sanitize(value):
    if isinstance(value, str) and value and value[0] in CSV_INJECTION_CHARS:
        return "'" + value
    return value


class FadminTable(tables.Table):
    class Meta:
        template_name = "django_tables_2_bootstrap.html"
        attrs = {
            "class": "govuk-table finance-table",
            "thead": {"class": "govuk-table__head"},
            "tbody": {"class": "govuk-table__body"},
            "tr": {"class": "govuk-table__row"},
            "th": {"class": "govuk-table__header"},
            "td": {"class": "govuk-table__cell"},
            "tf": {"class": "govuk-table__cell"},
            "a": {"class": "govuk-link"},
        }
        empty_text = "There are no results matching your search criteria."

    def as_values(self, exclude_columns=None):
        rows = super().as_values(exclude_columns)

        # First row is the header.
        yield next(rows)

        for row in rows:
            yield [_sanitize(value) for value in row]
