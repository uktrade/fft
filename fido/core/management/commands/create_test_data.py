from costcentre.models import CostCentre, DepartmentalGroup, Directorate
from chartofaccountDIT.models import Analysis1, Analysis2, BudgetType, ExpenditureCategory, \
    NACCategory, NaturalCode, ProgrammeCode, ProjectCode
from treasuryCOA.models import L1Account, L2Account, L3Account, L4Account, L5Account

from django.core.management.base import BaseCommand

# group = Group code,  directorate list
#  directorate = directorate code,  cost centre list
#  costcentre = code
# The descriptions are generated from a counter

my_cc_list = [
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
    """Clear the Cost Centre, Directorate and Group tables, and create the test data"""
    clear_cost_centre_hierarchy()
    counter = 0
    for group in my_cc_list:
        group_obj = DepartmentalGroup.objects.create(group_code=group[0], active=True,
                                                     group_name='Group ' + str(counter))
        counter += 1
        for dir in group[1]:
            dir_obj = Directorate.objects.create(directorate_code=dir[0], active=True,
                                                 directorate_name='Directorate ' + str(counter),
                                                 group=group_obj)
            counter += 1
            for cc in dir[1]:
                cc_obj = CostCentre.objects.create(cost_centre_code=cc, active=True,
                                                   cost_centre_name='Cost Centre ' + str(counter),
                                                   directorate=dir_obj
                                                   )
                cc_obj.save()
                counter += 1
    print('Test cost centre hierarchy created.')


def clear_programme():
    ProgrammeCode.objects.all().delete()


def create_programme():
    clear_programme()
    type = 'AME'
    budget = BudgetType.objects.get(pk=type)
    ProgrammeCode.objects.create(programme_code='338888', programme_description='Programme (' + type + ')',
                                 active=True, budget_type_fk=budget)
    type = 'DEL'
    budget = BudgetType.objects.get(pk=type)
    ProgrammeCode.objects.create(programme_code='338889', programme_description='Programme (' + type + ')',
                                 active=True, budget_type_fk=budget)
    type = 'ADMIN'
    budget = BudgetType.objects.get(pk=type)
    ProgrammeCode.objects.create(programme_code='338887', programme_description='Programme (' + type + ')',
                                 active=True, budget_type_fk=budget)
    print('Test programme codes created.')


def clear_analysis1():
    Analysis1.objects.all().delete()


def create_analysis1():
    clear_analysis1()
    Analysis1.objects.create(active=True, analysis1_code='10001', analysis1_description='Analysis 1 - 0')
    Analysis1.objects.create(active=True, analysis1_code='10002', analysis1_description='Analysis 1 - 1')
    Analysis1.objects.create(active=True, analysis1_code='10004', analysis1_description='Analysis 1 - 2')
    Analysis1.objects.create(active=True, analysis1_code='10005', analysis1_description='Analysis 1 - 3')
    Analysis1.objects.create(active=True, analysis1_code='10006', analysis1_description='Analysis 1 - 4')
    print('Test Analysis 1 codes created.')


def clear_analysis2():
    Analysis2.objects.all().delete()


def create_analysis2():
    clear_analysis2()
    Analysis2.objects.create(active=True, analysis2_code='40001', analysis2_description='Analysis 2 - 0')
    Analysis2.objects.create(active=True, analysis2_code='40002', analysis2_description='Analysis 2 - 1')
    Analysis2.objects.create(active=True, analysis2_code='40004', analysis2_description='Analysis 2 - 2')
    Analysis2.objects.create(active=True, analysis2_code='40005', analysis2_description='Analysis 2 - 3')
    Analysis2.objects.create(active=True, analysis2_code='40006', analysis2_description='Analysis 2 - 4')
    print('Test Analysis 2 codes created.')


def clear_project():
    ProjectCode.objects.all().delete()


def create_project():
    clear_project()
    ProjectCode.objects.create(active=True, project_code=5000, project_description='Project 1')
    ProjectCode.objects.create(active=True, project_code=5001, project_description='Project 2')
    ProjectCode.objects.create(active=True, project_code=5002, project_description='Project 3')
    ProjectCode.objects.create(active=True, project_code=5003, project_description='Project 4')
    ProjectCode.objects.create(active=True, project_code=5004, project_description='Project 5')
    print('Test project codes created.')


def clear_naturalaccount():
    # clear the NAC budget field before clearing the nac
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


def create_nac_group(cat, l5, cat_description, nac_base, howmany):
    budg = ExpenditureCategory.objects.create(
        active=True,
        grouping_description=cat_description,
        description='Expenditure: ' + cat_description,
        further_description='',
        NAC_category=cat
    )
    nac = NaturalCode.objects.create(
        active=True,
        natural_account_code=nac_base,
        natural_account_code_description='NAC  ' + cat_description + ' - budget',
        used_for_budget=True, account_L5_code=l5,
        expenditure_category=budg
    )

    budg.linked_budget_code = nac
    budg.save()
    for x in range(howmany):
        nac_base += 1
        nac = NaturalCode.objects.create(active=True, natural_account_code=nac_base,
                                         natural_account_code_description='NAC ' + cat_description + ' ' + str(x),
                                         used_for_budget=False, account_L5_code=l5, expenditure_category=budg)


def create_natural_accounts():
    clear_naturalaccount()
    # Create the dummy treasury structures
    l1 = L1Account.objects.create(active=True, account_l1_code=90000000, account_l1_long_name='L1 account',
                                  account_code='AI', account_l0_code='AI')

    l2 = L2Account.objects.create(active=True, account_l2_code=71000000, account_l2_long_name='L2 account',
                                  account_l1=l1)
    l3 = L3Account.objects.create(active=True, account_l3_code=71100000, account_l3_long_name='L3 account',
                                  account_l2=l2)
    l4 = L4Account.objects.create(active=True, account_l4_code=71110000, account_l4_long_name='L4 account',
                                  account_l3=l3)
    l5_res = L5Account.objects.create(active=True, account_l5_code=71111000, account_l5_long_name='L5 account',
                                      account_l4=l4, economic_budget_code='RESOURCE')

    l5_cap = L5Account.objects.create(active=True, account_l5_code=71112000, account_l5_long_name='L5 account',
                                      account_l4=l4, economic_budget_code='CAPITAL')

    # use real values for NAC categories. Easier than inventing some
    cat = NACCategory.objects.create(active=True, NAC_category_description='Pay')
    create_nac_group(cat, l5_res, 'Contractors (Pay)', 71111000, 5)

    cat = NACCategory.objects.create(active=True, NAC_category_description='NonCash')
    create_nac_group(cat, l5_res, 'Provisions', 71112000, 2)

    cat = NACCategory.objects.create(active=True, NAC_category_description='NonPay')
    create_nac_group(cat, l5_res, 'Staff Welfare', 71113000, 2)
    create_nac_group(cat, l5_res, 'Estates', 71114000, 1)
    create_nac_group(cat, l5_res, 'Grant', 71115000, 4)

    cat = NACCategory.objects.create(active=True, NAC_category_description='Capital')
    create_nac_group(cat, l5_cap, 'Estates (Capital)', 71121000, 4)

    print('Test natural account codes created.')


def clear_all():
    clear_cost_centre_hierarchy()
    clear_programme()
    clear_analysis1()
    clear_analysis2()
    clear_project()
    clear_naturalaccount()
    print('Test data removed.')


def create_all():
    create_cost_centre_hierarchy()
    create_programme()
    create_analysis1()
    create_analysis2()
    create_project()
    create_natural_accounts()


TEST_TYPE = {
    'CostCentre': create_cost_centre_hierarchy,
    'Clear': clear_all,
    'Programme': create_programme,
    'NAC': create_natural_accounts,
    'Analysis1': create_analysis1,
    'Analysis2': create_analysis2,
    'Project': create_project,
    'ClearDB': clear_all,
    'All': create_all
}


class Command(BaseCommand):
    help = 'Create test data. Allowed types are - All - ' + ' - '.join(TEST_TYPE.keys())

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
