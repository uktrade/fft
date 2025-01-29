import os
import pytest
from django.core.files import File

from chartofaccountDIT.test.factories import  ProgrammeCodeFactory
from costcentre.test.factories import CostCentreFactory
from gifthospitality.test.factories import GradeFactory
from ...services.ingest import import_payroll

@pytest.fixture(autouse=True)
def setup(db):
    cost_centre_codes=[888812,888813,888814]
    programme_codes=["338887","338888","338889"]
    grade_codes=["SEO",
            "SCS",
            "HEO",
            "Grade 7",
            "Grade 6",
            "Faststream",
            "EO",
            "Contractor",
            "AO",
            "AA"]
    cost_centres = [CostCentreFactory(cost_centre_code=id) for id in cost_centre_codes]
    programmes=[ProgrammeCodeFactory(programme_code=id) for id in programme_codes]
    grades=[GradeFactory(grade=id) for id in grade_codes]
    yield  


def test_ingest_payroll_success(db):
    """Testing valid records"""
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_assets')
    csv_file = os.path.join(test_data_dir, 'valid_records.csv')
    with open(csv_file, 'rb') as f:
        try:
            result = import_payroll(File(f))
            print(result)
        except Exception as e:
                        result = {
                        
                                'created': [],
                                'updated': [],
                                'failed': [],
                                'error': str(e)
                             }
        assert len(result.get('failed'))== 0
        assert result.get('error') is None
        assert result.get('created')==15  

def test_ingest_payroll_failed_record(db):
    """Testing failed records"""
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_assets')
    csv_file = os.path.join(test_data_dir, 'mixed_records.csv')
    with open(csv_file, 'rb') as f:
        try:
            result = import_payroll(File(f))
        except Exception as e:
                        result = {
                        
                                'created': [],
                                'updated': [],
                                'failed': [],
                                'error': str(e)
                             }
        assert result.get('failed') is not None

def test_ingest_payroll_error(db):
    """Testing mall structured  csv file"""
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_assets')
    csv_file = os.path.join(test_data_dir, 'error.csv')
    with open(csv_file, 'rb') as f:
        try:
            result = import_payroll(File(f))
        except Exception as e:
                        result = {
                        
                                'created': [],
                                'updated': [],
                                'failed': [],
                                'error': str(e)
                             }
        print(result)
        assert result.get('error') is not None

def test_ingest_payroll_update(db):
    """Testing update record functionality"""
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_assets')
    csv_file = os.path.join(test_data_dir, 'valid_records.csv')
    with open(csv_file, 'rb') as f:
        try:
            result = import_payroll(File(f))
            result = import_payroll(File(f))
        except Exception as e:
                        result = {
                        
                                'created': [],
                                'updated': [],
                                'failed': [],
                                'error': str(e)
                             }
        assert  len(result.get('failed'))== 0
        assert result.get('error') is None
        assert result.get('updated')==15  
        assert result.get('created')==0  