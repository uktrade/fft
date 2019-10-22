from costcentre.models import CostCentre, DepartmentalGroup, Directorate

import factory


class DepartmentalGroupFactory(factory.DjangoModelFactory):
    """
        Define DepartmentalGroup Factory
    """

    class Meta:
        model = DepartmentalGroup


class DirectorateFactory(factory.DjangoModelFactory):
    """
        Define Directorate Factory
    """

    class Meta:
        model = Directorate

    group = factory.SubFactory(DepartmentalGroupFactory)


class CostCentreFactory(factory.DjangoModelFactory):
    """
        Define CostCentre Factory
    """

    class Meta:
        model = CostCentre

    directorate = factory.SubFactory(DirectorateFactory)
