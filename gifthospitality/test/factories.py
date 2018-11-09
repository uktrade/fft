from gifthospitality.models import GiftsAndHospitality, GiftsAndHospitalityCategory, \
    GiftsAndHospitalityClassification, GiftsAndHospitalityCompany

import factory


class GiftsAndHospitalityFactory(factory.DjangoModelFactory):
    """
        Define GiftsAndHospitality Factory
    """

    class Meta:
        model = GiftsAndHospitality


class GiftsAndHospitalityCategoryFactory(factory.DjangoModelFactory):
    """
        Define GiftsAndHospitalityCategory Factory
    """

    class Meta:
        model = GiftsAndHospitalityCategory



class GiftsAndHospitalityClassificationFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = GiftsAndHospitalityClassification


class GiftsAndHospitalityCompanyFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = GiftsAndHospitalityCompany

