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


def add_finance_admin_permissions(apps, schema_editor):
    add_all_permissions()
    # Finance admins
    finance_adminstrators, _ = Group.objects.get_or_create(
        name='Finance Administrator',
    )
    permission = Permission.objects.get(
        codename="view_logentry",
    )
    finance_adminstrators.permissions.add(
        permission,
    )


class Migration(migrations.Migration):
    dependencies = [("core", "0007_auto_20200826_0813")]

    operations = [
        migrations.RunPython(add_finance_admin_permissions),
    ]
