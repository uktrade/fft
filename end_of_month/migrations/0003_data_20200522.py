from django.db import migrations


def populate_end_of_month(apps, schema_editor):
    EndOfMonthModel = apps.get_model("end_of_month", "EndOfMonthStatus")
    for m in range(1, 16):
        obj = EndOfMonthModel.objects.create(archived_period_id=m)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("forecast", "0002_data_20200522"),
        ("end_of_month", "0002_auto_20200522_1028"),
    ]
    operations = [migrations.RunPython(populate_end_of_month)]
