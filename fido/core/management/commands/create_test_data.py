from costcentre.models import CostCentre, DepartmentalGroup, Directorate
from chartofaccountDIT.models import Analysis1, Analysis2, BudgetType, ExpenditureCategory, \
    NACCategory, NaturalCode, ProgrammeCode, ProjectCode
from treasuryCOA.models import L1Account, L2Account, L3Account, L4Account, L5Account

from django.core.management.base import BaseCommand

# group = Group code,  directorate list
#  directorate = directorate code,  cost centre list
#  costcentre = code
# The descriptions are generated from a counter

cost_centre_hierarchy = [
    ['8888AA', [['88881A', [888811, 888812, 888813]],
                ['88882A', [888821, 888822, 888823]]
                ]],
    ['8888BB', [['88881B', [888831, 888832, 888833]],
                ['88882B', [888841, 888842, 888843]],
                ['88883C', [888851, 888852, 888853]],
                ]]]


def clear_cost_centre_hierarchy():
    CostCentre.objects.all().delete()
    Directorate.objects.all().delete()
    DepartmentalGroup.objects.all().delete()


def create_cost_centre_hierarchy():
    """Clear the Cost Centre, Directorate and Group tables, and create the stub data"""
    clear_cost_centre_hierarchy()
    counter = 0
    for departmental_group_code in cost_centre_hierarchy:
        departmental_group = DepartmentalGroup.objects.create(
            group_code=departmental_group_code[0],
            active=True,
            group_name='Departmental Group {}'.format(counter)
        )
        counter += 1
        for directorate_code in departmental_group_code[1]:
            directorate = Directorate.objects.create(
                directorate_code=directorate_code[0],
                active=True,
                directorate_name='Directorate {}'.format(counter),
                group=departmental_group
            )
            counter += 1
            for cost_centre_code in directorate_code[1]:
                CostCentre.objects.create(
                    cost_centre_code=cost_centre_code, active=True,
                    cost_centre_name='Cost Centre {}'.format(counter),
                    directorate=directorate
                )
                counter += 1
    print('Test cost centre hierarchy created.')


def clear_programme_codes():
    ProgrammeCode.objects.all().delete()


def create_programme_codes():
    clear_programme_codes()
    budget_type_code = 'AME'
    budget_type = BudgetType.objects.get(pk=budget_type_code)
    ProgrammeCode.objects.create(
        programme_code='338888',
        programme_description='Programme ({})'.format(budget_type_code),
        active=True,
        budget_type_fk=budget_type
    )
    budget_type_code = 'DEL'
    budget_type = BudgetType.objects.get(pk=budget_type_code)
    ProgrammeCode.objects.create(
        programme_code='338889',
        programme_description='Programme ({})'.format(budget_type_code),
        active=True,
        budget_type_fk=budget_type
    )
    budget_type_code = 'ADMIN'
    budget_type = BudgetType.objects.get(pk=budget_type_code)
    ProgrammeCode.objects.create(
        programme_code='338887',
        programme_description='Programme ({})'.format(budget_type_code),
        active=True,
        budget_type_fk=budget_type
    )
    print('Stub programme codes created.')


def clear_analysis1_codes():
    Analysis1.objects.all().delete()


def create_analysis1_codes():
    clear_analysis1_codes()
    Analysis1.objects.create(active=True, analysis1_code='10001', analysis1_description='Analysis 1 - 0')
    Analysis1.objects.create(active=True, analysis1_code='10002', analysis1_description='Analysis 1 - 1')
    Analysis1.objects.create(active=True, analysis1_code='10004', analysis1_description='Analysis 1 - 2')
    Analysis1.objects.create(active=True, analysis1_code='10005', analysis1_description='Analysis 1 - 3')
    Analysis1.objects.create(active=True, analysis1_code='10006', analysis1_description='Analysis 1 - 4')
    print('Test Analysis 1 codes created.')


def clear_analysis2_codes():
    Analysis2.objects.all().delete()


def create_analysis2_codes():
    clear_analysis2_codes()
    Analysis2.objects.create(active=True, analysis2_code='40001', analysis2_description='Analysis 2 - 0')
    Analysis2.objects.create(active=True, analysis2_code='40002', analysis2_description='Analysis 2 - 1')
    Analysis2.objects.create(active=True, analysis2_code='40004', analysis2_description='Analysis 2 - 2')
    Analysis2.objects.create(active=True, analysis2_code='40005', analysis2_description='Analysis 2 - 3')
    Analysis2.objects.create(active=True, analysis2_code='40006', analysis2_description='Analysis 2 - 4')
    print('Test Analysis 2 codes created.')


# TODO put everything in class
def clear_project_codes():
    ProjectCode.objects.all().delete()


def create_project_codes():
    clear_project_codes()
    ProjectCode.objects.create(active=True, project_code=5000, project_description='Project 1')
    ProjectCode.objects.create(active=True, project_code=5001, project_description='Project 2')
    ProjectCode.objects.create(active=True, project_code=5002, project_description='Project 3')
    ProjectCode.objects.create(active=True, project_code=5003, project_description='Project 4')
    ProjectCode.objects.create(active=True, project_code=5004, project_description='Project 5')
    print('Test project codes created.')


# TODO rename model NaturalCode to NaturalAccountCode
# TODO check CASCADE in model
def clear_natural_account_codes():
    # clear the NAC budget field in expenditure codes before clearing the natural account codes
    q = ExpenditureCategory.objects.all()
    for q1 in q:
        q1.linked_budget_code = None
        q1.save()
    NaturalCode.objects.all().delete()
    ExpenditureCategory.objects.all().delete()
    NACCategory.objects.all().delete()
    L5Account.objects.all().delete()
    L4Account.objects.all().delete()
    L3Account.objects.all().delete()
    L2Account.objects.all().delete()
    L1Account.objects.all().delete()


def create_natural_account_code_expenditure_group(
        nac_category,
        l5,
        cat_description,
        nac_base,
        howmany
):
    expenditure_category = ExpenditureCategory.objects.create(
        active=True,
        grouping_description=cat_description,
        description='Expenditure: {}'.format(cat_description),
        further_description='',
        NAC_category=nac_category
    )
    natural_account_code = NaturalCode.objects.create(
        active=True,
        natural_account_code=nac_base,
        natural_account_code_description='NAC  {} - budget'.format(cat_description),
        used_for_budget=True, account_L5_code=l5,
        expenditure_category=expenditure_category
    )
    expenditure_category.linked_budget_code = natural_account_code
    expenditure_category.save()
    for x in range(howmany):
        nac_base += 1
        NaturalCode.objects.create(
            active=True,
            natural_account_code=nac_base,
            natural_account_code_description='NAC {} {}'.format(cat_description, x),
            used_for_budget=False,
            account_L5_code=l5,
            expenditure_category=expenditure_category
        )


# TODO change model name L1Account to Level1Account
def create_natural_accounts():
    clear_natural_account_codes()
    # Create the dummy treasury structures
    l1_account = L1Account.objects.create(
        active=True,
        account_l1_code=90000000,
        account_l1_long_name='L1 account',
        account_code='AI',
        account_l0_code='AI'
    )
    l2_account = L2Account.objects.create(
        active=True,
        account_l2_code=71000000,
        account_l2_long_name='L2 account',
        account_l1=l1_account
    )
    l3_account = L3Account.objects.create(
        active=True,
        account_l3_code=71100000,
        account_l3_long_name='L3 account',
        account_l2=l2_account
    )
    l4_account = L4Account.objects.create(
        active=True,
        account_l4_code=71110000,
        account_l4_long_name='L4 account',
        account_l3=l3_account
    )
    l5_account_resource = L5Account.objects.create(
        active=True,
        account_l5_code=71111000,
        account_l5_long_name='L5 account',
        account_l4=l4_account,
        economic_budget_code='RESOURCE'
    )
    l5_account_capital = L5Account.objects.create(
        active=True,
        account_l5_code=71112000,
        account_l5_long_name='L5 account',
        account_l4=l4_account,
        economic_budget_code='CAPITAL'
    )
    # use real values for NAC categories. Easier than inventing some
    nac_category = NACCategory.objects.create(active=True, NAC_category_description='Pay')
    create_natural_account_code_expenditure_group(nac_category, l5_account_resource, 'Contractors (Pay)', 71111000, 5)

    nac_category = NACCategory.objects.create(active=True, NAC_category_description='NonCash')
    create_natural_account_code_expenditure_group(nac_category, l5_account_resource, 'Provisions', 71112000, 2)

    nac_category = NACCategory.objects.create(active=True, NAC_category_description='NonPay')
    create_natural_account_code_expenditure_group(nac_category, l5_account_resource, 'Staff Welfare', 71113000, 2)
    create_natural_account_code_expenditure_group(nac_category, l5_account_resource, 'Estates', 71114000, 1)
    create_natural_account_code_expenditure_group(nac_category, l5_account_resource, 'Grant', 71115000, 4)

    nac_category = NACCategory.objects.create(active=True, NAC_category_description='Capital')
    create_natural_account_code_expenditure_group(nac_category, l5_account_capital, 'Estates (Capital)', 71121000, 4)

    print('Test natural account codes created.')


def clear_all():
    clear_cost_centre_hierarchy()
    clear_programme_codes()
    clear_analysis1_codes()
    clear_analysis2_codes()
    clear_project_codes()
    clear_natural_account_codes()
    print('Test data removed.')


def create_all():
    create_cost_centre_hierarchy()
    create_programme_codes()
    create_analysis1_codes()
    create_analysis2_codes()
    create_project_codes()
    create_natural_accounts()


TEST_TYPE = {
    'CostCentre': create_cost_centre_hierarchy,
    'Clear': clear_all,
    'Programme': create_programme_codes,
    'NAC': create_natural_accounts,
    'Analysis1': create_analysis1_codes,
    'Analysis2': create_analysis2_codes,
    'Project': create_project_codes,
    'ClearDB': clear_all,
    'All': create_all
}


# TODO Deafult to all when no argument is passed
# TODO use try in handle
class Command(BaseCommand):
    help = 'Create stub data. Allowed types are - All - ' + ' - '.join(TEST_TYPE.keys())

    def add_arguments(self, parser):
        parser.add_argument('type')

    def handle(self, *args, **options):
        createtype = options.get('type')
        # The modified save writes the current user to the log, but the user is not available while we are running a command.
        # So set  the test flag to stop writing to the log
        import core
        core._called_from_test = True
        TEST_TYPE[createtype]()
        core._called_from_test = False
