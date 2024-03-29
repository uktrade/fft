# Generated by Django 3.0.3 on 2021-02-26 18:02

from django.db import migrations


def fix_calendar_codes(apps, schema_editor):
    PeriodModel = apps.get_model("forecast", "FinancialPeriod")
    # Fix the calendar code for the adjustemnt periods.
    # Pretend they are extra months!
    for period_code in range(13, 16):
        period_obj = PeriodModel.objects.get(financial_period_code=period_code)
        period_obj.period_calendar_code = period_code
        period_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("forecast", "0004_auto_20200820_0751"),
    ]

    operations = [
        migrations.RunPython(fix_calendar_codes),
    ]
