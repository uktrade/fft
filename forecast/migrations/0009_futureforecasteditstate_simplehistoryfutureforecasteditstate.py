# Generated by Django 3.2.13 on 2022-04-27 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models

def create_future_forecast_lock(apps, schema_editor):
    FutureForecastEditState = apps.get_model('forecast', 'FutureForecastEditState')
    FutureForecastEditState.objects.create()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecast', '0008_amend_views_20210802_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='FutureForecastEditState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('closed', models.BooleanField(default=False, help_text='Ticking this option will close future forecast editing access to all non finance staff. Future forecast editing is still available to Finance business partners/BSCEs and admin.')),
                ('lock_date', models.DateField(blank=True, help_text="The future forecast editing is locked from the date entered. The future forecast editing will remain locked to users without 'unlocked' user status, until the date is removed from the input field above.", null=True, verbose_name='Lock future forecast')),
            ],
            options={
                'verbose_name_plural': 'Future forecast edit state',
                'permissions': [('can_set_future_edit_lock', 'Can set future edit lock'), ('can_edit_future_whilst_closed', 'Can edit future forecasts whilst system is closed'), ('can_edit_future_whilst_locked', 'Can edit future forecasts whilst system is locked')],
                'default_permissions': ('view', 'change'),
            },
        ),
        migrations.CreateModel(
            name='SimpleHistoryFutureForecastEditState',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('closed', models.BooleanField(default=False, help_text='Ticking this option will close future forecast editing access to all non finance staff. Future forecast editing is still available to Finance business partners/BSCEs and admin.')),
                ('lock_date', models.DateField(blank=True, help_text="The future forecast editing is locked from the date entered. The future forecast editing will remain locked to users without 'unlocked' user status, until the date is removed from the input field above.", null=True, verbose_name='Lock future forecast')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical future forecast edit state',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.RunPython(create_future_forecast_lock),
    ]