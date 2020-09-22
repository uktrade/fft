from django.test import TestCase

from chartofaccountDIT.import_archived_from_csv import (
    import_archived_analysis1,
    import_archived_analysis2,
    import_archived_programme,
    import_archived_project,
)
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.test.test_base import RequestFactoryBase

from forecast.import_csv import WrongChartOFAccountCodeException


class UploadArchiveAnalysis1Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Analysis 1 Code,Contract Name,Supplier,PC Reference"
        data_row = "00012,Test Contract,Test Supplier,Test PC Reference"

        assert ArchivedAnalysis1.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_analysis1(csvfile, 2019)
        assert ArchivedAnalysis1.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Analysis,Contract Name,Supplier,PC Reference"
        data_row = "00012,Test Contract,Test Supplier,Test PC Reference"

        assert ArchivedAnalysis1.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_analysis1(csvfile, 2019)
        assert ArchivedAnalysis1.objects.all().count() == 0


class UploadArchiveAnalysis2Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Market Code,Market Description"
        data_row = "00012,NeverLand"

        assert ArchivedAnalysis2.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_analysis2(csvfile, 2019)
        assert ArchivedAnalysis2.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Market Code,Description"
        data_row = "00012,NeverLand"

        assert ArchivedAnalysis2.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_analysis2(csvfile, 2019)
        assert ArchivedAnalysis2.objects.all().count() == 0


class UploadProjectTest(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Project Code,Project Description"
        data_row = "00012,Cyber Security"

        assert ArchivedProjectCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_project(csvfile, 2019)
        assert ArchivedProjectCode.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Code,Project Description"
        data_row = "00012,Cyber Security"

        assert ArchivedProjectCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_project(csvfile, 2019)
        assert ArchivedProjectCode.objects.all().count() == 0


class UploadProgrammeTest(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        # I could use 'get_col_from_obj_key' to generate the header from the key
        # used to upload the data, but for the sake of clarity I decided to
        # define the header here. So, if the object key is changed, this test may fail.
        header_row = "Programme Code,Programme Description,Type"
        data_row = "00012,Ame Programme,AME"

        assert ArchivedProgrammeCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_programme(csvfile, 2019)
        assert ArchivedProgrammeCode.objects.all().count() == 1

    def test_wrong_header(self):
        header_row = "Code,Programme Description,Type"
        data_row = "00012,Ame Programme,AME"

        assert ArchivedProgrammeCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_project(csvfile, 2019)
        assert ArchivedProgrammeCode.objects.all().count() == 0
