from django.test import TestCase

from core.test.test_base import RequestFactoryBase

from costcentre.import_archived_from_csv import import_archived_cost_centre
from costcentre.models import ArchivedCostCentre

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import ArchiveYearError


class UploadArchiveCostCentreTest(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = (
            "Cost Centre Code,Cost Centre Description,"
            "Directorate Code,Directorate Description,"
            "Group Code,Group Description"
        )
        data_row = (
            "109045,Test Cost Centre," "10900T,Test Directorate," "1090TT,Test Group"
        )

        assert ArchivedCostCentre.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_cost_centre(csvfile, 2019)
        assert ArchivedCostCentre.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = (
            "Cost Centre,Cost Centre Description,"
            "Directorate Code,Directorate Description,"
            "Group Code,Group Description"
        )
        data_row = (
            "109045,Test Cost Centre," "10900T,Test Directorate," "1090TT,Test Group"
        )

        assert ArchivedCostCentre.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_cost_centre(csvfile, 2019)
        assert ArchivedCostCentre.objects.all().count() == 0

    def test_wrong_year(self):
        header_row = (
            "Cost Centre Code,Cost Centre Description,"
            "Directorate Code,Directorate Description,"
            "Group Code,Group Description"
        )
        data_row = (
            "109045,Test Cost Centre," "10900T,Test Directorate," "1090TT,Test Group"
        )

        assert ArchivedCostCentre.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_cost_centre(csvfile, 2000)
        assert ArchivedCostCentre.objects.all().count() == 0
