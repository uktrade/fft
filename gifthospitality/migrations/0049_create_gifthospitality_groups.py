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


def create_gift_hospitality_groups(apps, schema_editor):
    add_all_permissions()

    # Gift and Hospitality Admin
    gift_hospitality_admin, _ = Group.objects.get_or_create(
        name='Gift and Hospitality Admin',
    )

class Migration(migrations.Migration):
    dependencies = [
        ("gifthospitality", "0048_auto_20200416_1346"),
    ]

    operations = [
        migrations.RunPython(create_gift_hospitality_groups),
    ]
