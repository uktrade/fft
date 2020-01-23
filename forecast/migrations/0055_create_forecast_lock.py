from django.db import migrations


def create_forecast_lock(apps, schema_editor):
    ForecastEditLock = apps.get_model('forecast', 'ForecastEditLock')
    ForecastEditLock.objects.create()


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0054_auto_20200123_1103'),
    ]

    operations = [
        migrations.RunPython(create_forecast_lock),
    ]
