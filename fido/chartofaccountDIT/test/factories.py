from chartofaccountDIT.models import Analysis1, Analysis2, BudgetType, CommercialCategory, ExpenditureCategory, \
    FCOMapping, \
    HistoricalAnalysis1, HistoricalAnalysis2, HistoricalCommercialCategory, HistoricalExpenditureCategory, \
    HistoricalFCOMapping, HistoricalInterEntity, HistoricalNaturalCode, HistoricalProgrammeCode, \
    HistoricalProjectCode, InterEntity, InterEntityL1, NACCategory, NaturalCode, \
    OperatingDeliveryCategory, ProgrammeCode, ProjectCode

import factory


class Analysis1Factory(factory.DjangoModelFactory):
    """
    Define Analysis1 Factory
    """

    class Meta:
        model = Analysis1


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


class HistoricalNaturalCodeFactory(factory.DjangoModelFactory):
    """
    Define HistoricalNaturalCode Factory
    """

    class Meta:
        model = HistoricalNaturalCode


class BudgetTypeFactory(factory.DjangoModelFactory):
    """
    Define BudgetType Factory
    """

    class Meta:
        model = BudgetType


class ProgrammeCodeFactory(factory.DjangoModelFactory):
    """
    Define ProgrammeCode Factory
    """

    class Meta:
        model = ProgrammeCode


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
