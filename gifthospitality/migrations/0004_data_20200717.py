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


def add_gandh_admin_permissions(apps, schema_editor):
    add_all_permissions()

    # Finance admins
    gift_hospitality_admin, _ = Group.objects.get_or_create(
        name='Gift and Hospitality Admin',
    )

    assign_permissions(
        gift_hospitality_admin, [
            # admin permissions follow
            "can_view_all_gifthospitality"
        ],
    )


class Migration(migrations.Migration):
    dependencies = [("gifthospitality", "0003_auto_20200602_1300")]

    operations = [
        migrations.RunPython(add_gandh_admin_permissions),
    ]
