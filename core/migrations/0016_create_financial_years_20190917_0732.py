from django.db import migrations
from core.myutils import get_current_financial_year

fields = ["financial_year", "financial_year_display", "current"]

financial_years = [
    [2019, "2019-20", False],
    [2020, "2020-21", False],
    [2021, "2021-22", False],
]


def populate_financial_years(apps, schema_editor):
    financial_year_model = apps.get_model("core", "FinancialYear")
    current_financial_year = get_current_financial_year()
    for y in financial_years:
        d = dict(zip(fields, y))
        if d["financial_year"] == current_financial_year:
            d["current"] = True
        obj, created = financial_year_model.objects.get_or_create(**d)


class Migration(migrations.Migration):
    dependencies = [("core", "0015_auto_20200130_1135")]

    operations = [migrations.RunPython(populate_financial_years)]
