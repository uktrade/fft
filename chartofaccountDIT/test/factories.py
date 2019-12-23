import factory

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    HistoricalAnalysis1,
    HistoricalAnalysis2,
    HistoricalCommercialCategory,
    HistoricalExpenditureCategory,
    HistoricalFCOMapping,
    HistoricalInterEntity,
    HistoricalNaturalCode,
    HistoricalProgrammeCode,
    HistoricalProjectCode,
    InterEntity,
    InterEntityL1,
    NACCategory,
    NaturalCode,
    OperatingDeliveryCategory,
    ProgrammeCode,
    ProjectCode,
)


class Analysis1Factory(factory.DjangoModelFactory):
    """
    Define Analysis1 Factory
    """

    class Meta:
        model = Analysis1

    active = True


class HistoricalAnalysis1Factory(factory.DjangoModelFactory):
    """
    Define HistoricalAnalysis1 Factory
    """

    class Meta:
        model = HistoricalAnalysis1


class Analysis2Factory(factory.DjangoModelFactory):
    """
    Define Analysis2 Factory
    """

    class Meta:
        model = Analysis2

    active = True


class HistoricalAnalysis2Factory(factory.DjangoModelFactory):
    """
    Define HistoricalAnalysis2 Factory
    """

    class Meta:
        model = HistoricalAnalysis2


class NACCategoryFactory(factory.DjangoModelFactory):
    """
    Define NACCategory Factory
    """

    class Meta:
        model = NACCategory

    NAC_category_description = "Test NAC desc"


class OperatingDeliveryCategoryFactory(factory.DjangoModelFactory):
    """
    Define OperatingDeliveryCategory Factory
    """

    class Meta:
        model = OperatingDeliveryCategory


class ExpenditureCategoryFactory(factory.DjangoModelFactory):
    """
    Define ExpenditureCategory Factory
    """

    grouping_description = 'Test Budget Category'

    class Meta:
        model = ExpenditureCategory


class HistoricalExpenditureCategoryFactory(factory.DjangoModelFactory):
    """
    Define HistoricalExpenditureCategory Factory
    """

    class Meta:
        model = HistoricalExpenditureCategory


class CommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define CommercialCategory Factory
    """

    class Meta:
        model = CommercialCategory


class HistoricalCommercialCategoryFactory(factory.DjangoModelFactory):
    """
    Define HistoricalCommercialCategory Factory
    """

    class Meta:
        model = HistoricalCommercialCategory


class NaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define NaturalCode Factory
    """

    class Meta:
        model = NaturalCode

    active = True
    natural_account_code = 999999
    natural_account_code_description = "NAC description"
    used_for_budget = False


class HistoricalNaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define HistoricalNaturalCode Factory
    """

    class Meta:
        model = HistoricalNaturalCode


class ProgrammeCodeFactory(factory.django.DjangoModelFactory):
    """
    Define ProgrammeCode Factory
    """

    class Meta:
        model = ProgrammeCode

    active = True
    programme_code = "123456"
    programme_description = "Programme Test description"
    budget_type_fk = factory.Iterator(BudgetType.objects.all())


class HistoricalProgrammeCodeFactory(factory.DjangoModelFactory):
    """
    Define HistoricalProgrammeCode Factory
    """

    class Meta:
        model = HistoricalProgrammeCode


class InterEntityL1Factory(factory.DjangoModelFactory):
    """
    Define InterEntityL1 Factory
    """

    class Meta:
        model = InterEntityL1


class InterEntityFactory(factory.DjangoModelFactory):
    """
    Define InterEntity Factory
    """

    class Meta:
        model = InterEntity


class HistoricalInterEntityFactory(factory.DjangoModelFactory):
    """
    Define HistoricalInterEntity Factory
    """

    class Meta:
        model = HistoricalInterEntity


class ProjectCodeFactory(factory.DjangoModelFactory):
    """
    Define ProjectCode Factory
    """

    class Meta:
        model = ProjectCode

    active = True
    project_code = "5000"
    project_description = "Project Description"


class HistoricalProjectCodeFactory(factory.DjangoModelFactory):
    """
    Define HistoricalProjectCode Factory
    """

    class Meta:
        model = HistoricalProjectCode


class FCOMappingFactory(factory.DjangoModelFactory):
    """
    Define FCOMapping Factory
    """

    class Meta:
        model = FCOMapping


class HistoricalFCOMappingFactory(factory.DjangoModelFactory):
    """
    Define HistoricalFCOMapping Factory
    """

    class Meta:
        model = HistoricalFCOMapping
