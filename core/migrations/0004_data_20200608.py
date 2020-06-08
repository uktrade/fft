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


def add_finance_admin_permissions(apps, schema_editor):
    add_all_permissions()

    # Finance admins
    finance_adminstrators, _ = Group.objects.get_or_create(
        name='Finance Administrator',
    )

    assign_permissions(
        finance_adminstrators, [
            # admin permissions follow
            "change_naturalcode",
            "add_naturalcode",
            "change_analysis1",
            "add_analysis1",
            "change_commercialcategory",
            "add_commercialcategory",
            "change_fcomapping",
            "add_fcomapping",
            "change_interentity",
            "add_interentity",
            "change_interentityl1",
            "add_interentityl1",
            "change_operatingdeliverycategory",
            "add_operatingdeliverycategory",
            "change_programmecode",
            "add_programmecode",
            "change_projectcode",
            "add_projectcode",

        ],
    )


class Migration(migrations.Migration):
    dependencies = [("core", "0003_data_20200604")]

    operations = [
        migrations.RunPython(add_finance_admin_permissions),
    ]
