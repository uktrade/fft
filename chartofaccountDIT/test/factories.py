from factory.django import DjangoModelFactory

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    BudgetType,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    InterEntityL1,
    NACCategory,
    NaturalCode,
    OperatingDeliveryCategory,
    ProgrammeCode,
    ProjectCode,
)


class Analysis1Factory(DjangoModelFactory):
    """
    Define Analysis1 Factory
    """

    class Meta:
        model = Analysis1

    active = True


class HistoricalAnalysis1Factory(DjangoModelFactory):
    class Meta:
        model = ArchivedAnalysis1


class Analysis2Factory(DjangoModelFactory):
    """
    Define Analysis2 Factory
    """

    class Meta:
        model = Analysis2

    active = True


class HistoricalAnalysis2Factory(DjangoModelFactory):
    class Meta:
        model = ArchivedAnalysis2


class NACCategoryFactory(DjangoModelFactory):
    """
    Define NACCategory Factory
    """

    class Meta:
        model = NACCategory

    NAC_category_description = factory.Faker("name")


class OperatingDeliveryCategoryFactory(DjangoModelFactory):
    """
    Define OperatingDeliveryCategory Factory
    """

    class Meta:
        model = OperatingDeliveryCategory


class ExpenditureCategoryFactory(DjangoModelFactory):
    """
    Define ExpenditureCategory Factory
    """

    grouping_description = "Test Budget Category"
    NAC_category = factory.SubFactory(NACCategoryFactory)

    class Meta:
        model = ExpenditureCategory


class HistoricalExpenditureCategoryFactory(DjangoModelFactory):
    grouping_description = "Test Archived Budget Category"

    class Meta:
        model = ArchivedExpenditureCategory


class CommercialCategoryFactory(DjangoModelFactory):
    """
    Define CommercialCategory Factory
    """

    active = True

    class Meta:
        model = CommercialCategory


class HistoricalCommercialCategoryFactory(DjangoModelFactory):
    active = True

    class Meta:
        model = ArchivedCommercialCategory


class NaturalCodeFactory(DjangoModelFactory):
    """
    Define NaturalCode Factory
    """

    class Meta:
        model = NaturalCode
        django_get_or_create = ("natural_account_code",)

    active = True
    natural_account_code = 999999
    natural_account_code_description = "NAC description"
    used_for_budget = False


class HistoricalNaturalCodeFactory(DjangoModelFactory):

    active = True
    natural_account_code = 87654321
    natural_account_code_description = "Historical NAC description"
    used_for_budget = False

    class Meta:
        model = ArchivedNaturalCode


class ProgrammeCodeFactory(DjangoModelFactory):
    """
    Define ProgrammeCode Factory
    """

    class Meta:
        model = ProgrammeCode
        django_get_or_create = ("programme_code",)

    active = True
    programme_code = "123456"
    programme_description = "Programme Test description"
    budget_type = factory.Iterator(BudgetType.objects.all())


class HistoricalProgrammeCodeFactory(DjangoModelFactory):
    """
    Define ArchivedProgrammeCode Factory
    """

    active = True
    programme_code = "654321"
    programme_description = "Programme Test description"
    budget_type = factory.Iterator(BudgetType.objects.all())

    class Meta:
        model = ArchivedProgrammeCode


class InterEntityL1Factory(DjangoModelFactory):
    """
    Define InterEntityL1 Factory
    """

    class Meta:
        model = InterEntityL1


class InterEntityFactory(DjangoModelFactory):
    """
    Define InterEntity Factory
    """

    active = True
    l1_value = factory.SubFactory(InterEntityL1Factory)

    class Meta:
        model = InterEntity


class HistoricalInterEntityFactory(DjangoModelFactory):
    active = True

    class Meta:
        model = ArchivedInterEntity


class ProjectCodeFactory(DjangoModelFactory):
    """
    Define ProjectCode Factory
    """

    class Meta:
        model = ProjectCode
        django_get_or_create = ("project_code",)

    active = True
    project_code = "5000"
    project_description = "Project Description"


class HistoricalProjectCodeFactory(DjangoModelFactory):
    """
    Define ArchivedProjectCode Factory
    """

    active = True
    project_code = "5000"
    project_description = "Project Description"

    class Meta:
        model = ArchivedProjectCode


class FCOMappingFactory(DjangoModelFactory):
    """
    Define FCOMapping Factory
    """

    fco_code = 123456
    active = True
    account_L6_code_fk = factory.SubFactory(NaturalCodeFactory)

    class Meta:
        model = FCOMapping


class HistoricalFCOMappingFactory(DjangoModelFactory):
    """
    Define ArchivedFCOMapping Factory
    """

    fco_code = 7891011
    account_L6_code = 98765432
    active = True

    class Meta:
        model = ArchivedFCOMapping
