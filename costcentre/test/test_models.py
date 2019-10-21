import pytest

from .factories import CostCentreFactory, DepartmentalGroupFactory, DirectorateFactory


# https://medium.com/@dwernychukjosh/testing-models-with-django-using-pytest-and-factory-boy-a2985adce7b3

@pytest.mark.django_db
def test_costcentre_model():
    group_fact = DepartmentalGroupFactory(group_code='G1', group_name = 'GroupName')
    directorate_fact = DirectorateFactory(directorate_code='D1', directorate_name='Finance', group=group_fact)
    costcentre_fact = CostCentreFactory(cost_centre_code='Test1', directorate=directorate_fact)
    assert costcentre_fact.cost_centre_code == 'Test1'
    assert costcentre_fact.directorate.directorate_name == 'Finance'
    assert costcentre_fact.directorate.group.group_name == 'GroupName'
