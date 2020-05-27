from django.db import migrations


def create_budget_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")
    BudgetType.objects.create(budget_type_key="DEL", budget_type="Programme DEL")
    BudgetType.objects.create(budget_type_key="AME", budget_type="Programme AME")
    BudgetType.objects.create(budget_type_key="ADMIN", budget_type="Admin")


def insert_budget_type_fk(apps, schema_editor):
    ProgrammeCode = apps.get_model("chartofaccountDIT", "ProgrammeCode")
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")
    for programme in ProgrammeCode.objects.all():
        programme.budget_type_fk = BudgetType.objects.get(
            budget_type=programme.budget_type
        )
        programme.save()


def update_1(apps, schema_editor):
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


def update_2(apps, schema_editor):
    NacCategory = apps.get_model("chartofaccountDIT", 'naccategory')

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="Pay")
    model_obj.NAC_category_display_order = 1
    model_obj.save()

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="NonPay")
    model_obj.NAC_category_display_order = 2
    model_obj.save()

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="NonCash")
    model_obj.NAC_category_display_order = 3
    model_obj.save()

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="Capital")
    model_obj.NAC_category_display_order = 4
    model_obj.save()

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="Contingency")
    model_obj.NAC_category_display_order = 5
    model_obj.save()

    model_obj, _ = NacCategory.objects.get_or_create(NAC_category_description="Remove")
    model_obj.NAC_category_display_order = 99
    model_obj.save()


class Migration(migrations.Migration):

    dependencies = [("chartofaccountDIT", "0001_initial")]

    operations = [
        migrations.RunPython(create_budget_types),
        migrations.RunPython(insert_budget_type_fk),
        migrations.RunPython(update_1),
        migrations.RunPython(update_2),
    ]
