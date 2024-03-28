from factory.django import DjangoModelFactory

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
)


class GiftsAndHospitalityFactory(DjangoModelFactory):
    """
    Define GiftsAndHospitality Factory
    """

    class Meta:
        model = GiftAndHospitality


class GiftsAndHospitalityCategoryFactory(DjangoModelFactory):
    """
    Define GiftsAndHospitalityCategory Factory
    """

    class Meta:
        model = GiftAndHospitalityCategory


class GiftsAndHospitalityClassificationFactory(DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityClassification


class GiftsAndHospitalityCompanyFactory(DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityCompany
