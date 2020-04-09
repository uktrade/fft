from django.db import migrations, models


def update(apps, schema_editor):
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")
    NaturalCode = apps.get_model('chartofaccountDIT', 'NaturalCode')

    natural_codes = NaturalCode.objects.filter(account_L5_code__isnull=False)
    for natural_code in natural_codes:
        natural_code.economic_budget_code = natural_code.account_L5_code.economic_budget_code
        natural_code.save()

    budget_type = BudgetType.objects.get(budget_type_key="DEL")
    budget_type.budget_type_display = "DEL"
    budget_type.budget_type_display_order = 1
    budget_type.budget_type_edit_display_order = 2
    budget_type.save()

    budget_type = BudgetType.objects.get(budget_type_key="AME", budget_type="Programme AME")
    budget_type.budget_type_display = "AME"
    budget_type.budget_type_display_order = 2
    budget_type.budget_type_edit_display_order = 3
    budget_type.save()

    budget_type = BudgetType.objects.get(budget_type_key="ADMIN", budget_type="Admin")
    budget_type.budget_type_display = "DEL"
    budget_type.budget_type_display_order = 1
    budget_type.budget_type_edit_display_order = 1
    budget_type.save()


class Migration(migrations.Migration):
    dependencies = [("chartofaccountDIT", "0049_auto_20200214_1117")]

    operations = [
        migrations.RunPython(update),
    ]
