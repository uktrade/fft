import pytest

from .factories import CostcentreFactory


# https://medium.com/@dwernychukjosh/testing-models-with-django-using-pytest-and-factory-boy-a2985adce7b3

@pytest.mark.django_db
def test_costcentre_model():
    #    directorate = DirectorateFactory(directorate_code='D1', directorate_name='Finance')
    costcentre = CostcentreFactory(cost_centre_code='Test1')
    assert costcentre.cost_centre_code == 'Test1'
