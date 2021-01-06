import factory

from faker import Faker

from core.models import FinancialYear

from costcentre.models import (
    ArchivedCostCentre,
    BSCEEmail,
    BusinessPartner,
    CostCentre,
    DepartmentalGroup,
    Directorate,
)

fake = Faker()


class DepartmentalGroupFactory(factory.DjangoModelFactory):
    """
        Define DepartmentalGroup Factory
    """

    class Meta:
        model = DepartmentalGroup
        django_get_or_create = ("group_code",)
    # Remove commas, because they break the test exporting csv data.
    group_name = fake.company().replace("'", " ")
    group_code = str(fake.pyint())
    active = True


class DirectorateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Directorate
        django_get_or_create = ("directorate_code",)

    directorate_name = fake.company().replace("'", " ")
    directorate_code = str(fake.pyint())
    group = factory.SubFactory(DepartmentalGroupFactory)
    active = True


class FinancialYearFactory(factory.DjangoModelFactory):
    class Meta:
        model = FinancialYear
        django_get_or_create = ("financial_year",)

    financial_year = 2019


class FinanceBusinessPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = BusinessPartner
        django_get_or_create = ("name", "surname")

    name = "test"
    surname = "FBP"


class BSCEFactory(factory.DjangoModelFactory):
    class Meta:
        model = BSCEEmail
        django_get_or_create = ("bsce_email",)

    bsce_email = "bsceuser@test.com"


class CostCentreFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = CostCentre
        django_get_or_create = ("cost_centre_code",)

    active = True
    directorate = factory.SubFactory(DirectorateFactory)
    cost_centre_code = 999999
    cost_centre_name = "Test Cost Centre"
    business_partner = factory.SubFactory(FinanceBusinessPartnerFactory)
    bsce_email = factory.SubFactory(BSCEFactory)


class ArchivedCostCentreFactory(factory.DjangoModelFactory):
    class Meta:
        model = ArchivedCostCentre

    active = True
    cost_centre_code = 999999
    cost_centre_name = "Test Cost Centre"
