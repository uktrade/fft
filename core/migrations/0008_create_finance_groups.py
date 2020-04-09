from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db import migrations

Permission = apps.get_model('auth', 'Permission')
Group = apps.get_model('auth', 'Group')


def add_all_permissions():
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None


def assign_permissions(group, permission_codenames):
    for permission_codename in permission_codenames:
        permission = Permission.objects.get(
            codename=permission_codename,
        )
        group.permissions.add(
            permission,
        )


def create_groups(apps, schema_editor):
    add_all_permissions()

    # Forecast viewers
    forecast_viewers, _ = Group.objects.get_or_create(
        name='Forecast viewers',
    )

    assign_permissions(
        forecast_viewers, [
            "can_view_forecasts",
        ]
    )

    # Finance Business Partners
    finance_business_partners, _ = Group.objects.get_or_create(
        name='Finance Business Partner/BSCE',

    )

    assign_permissions(
        finance_business_partners, [
            "can_view_forecasts",
            "can_edit_whilst_closed",
            "assign_edit_for_own_cost_centres",
            "change_costcentre",  # admin permission
        ],
    )

    # Finance admins
    finance_adminstrators, _ = Group.objects.get_or_create(
        name='Finance Administrator',
    )

    assign_permissions(
        finance_adminstrators, [
            "can_view_forecasts",
            "edit_forecast_all_cost_centres",
            "can_edit_whilst_locked",
            # admin permissions follow
            "change_costcentre",
            "change_user",
            "add_unlockedforecasteditor",
            "delete_unlockedforecasteditor",
            "view_unlockedforecasteditor",
            "view_forecasteditstate",
            "change_forecasteditstate",
        ],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_create_financial_years"),
        ("forecast", "0003_auto_20200403_0828"),
        ("costcentre", "0031_auto_20200403_0828"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
