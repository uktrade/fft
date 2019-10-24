import factory

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
)


class GiftsAndHospitalityFactory(factory.DjangoModelFactory):
    """
        Define GiftsAndHospitality Factory
    """

    class Meta:
        model = GiftAndHospitality


class GiftsAndHospitalityCategoryFactory(factory.DjangoModelFactory):
    """
        Define GiftsAndHospitalityCategory Factory
    """

    class Meta:
        model = GiftAndHospitalityCategory


class GiftsAndHospitalityClassificationFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityClassification


class GiftsAndHospitalityCompanyFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityCompany
