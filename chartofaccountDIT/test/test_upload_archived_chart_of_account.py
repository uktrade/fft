from django.test import TestCase

from chartofaccountDIT.import_archived_from_csv import (
    import_archived_analysis1,
    import_archived_analysis2,
    import_archived_nac,
    import_archived_programme,
    import_archived_project,
)
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedExpenditureCategory,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.test.test_base import RequestFactoryBase

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import ArchiveYearError


class UploadArchiveAnalysis1Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
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

    def test_wrong_year(self):
        header_row = "Analysis 1 Code,Contract Name,Supplier,PC Reference"
        data_row = "00012,Test Contract,Test Supplier,Test PC Reference"

        assert ArchivedAnalysis1.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_analysis1(csvfile, 2000)
        assert ArchivedAnalysis1.objects.all().count() == 0


class UploadArchiveAnalysis2Test(TestCase, RequestFactoryBase):
    def test_correct_data(self):
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

    def test_wrong_year(self):
        header_row = "Market Code,Market Description"
        data_row = "00012,NeverLand"

        assert ArchivedAnalysis2.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_analysis2(csvfile, 2000)
        assert ArchivedAnalysis2.objects.all().count() == 0


class UploadProjectTest(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        header_row = "Project Code,Project Description"
        data_row = "00012,Cyber Security"

        assert ArchivedProjectCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_project(csvfile, 2019)
        assert ArchivedProjectCode.objects.all().count() == 1

    def test_wrong_year(self):
        header_row = "Project Code,Project Description"
        data_row = "00012,Cyber Security"

        assert ArchivedProjectCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_project(csvfile, 2000)
        assert ArchivedProjectCode.objects.all().count() == 0

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
        header_row = "Programme Code,Programme Description,Type"
        data_row = "00012,Ame Programme,AME"

        assert ArchivedProgrammeCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_programme(csvfile, 2019)
        assert ArchivedProgrammeCode.objects.all().count() == 1

    def test_wrong_year(self):
        header_row = "Programme Code,Programme Description,Type"
        data_row = "00012,Ame Programme,AME"

        assert ArchivedProgrammeCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_project(csvfile, 2000)
        assert ArchivedProgrammeCode.objects.all().count() == 0

    def test_wrong_header(self):
        header_row = "Code,Programme Description,Type"
        data_row = "00012,Ame Programme,AME"

        assert ArchivedProgrammeCode.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_project(csvfile, 2019)
        assert ArchivedProgrammeCode.objects.all().count() == 0


class UploadNACTest(TestCase, RequestFactoryBase):
    def test_correct_data(self):
        header_row = "Expenditure Type,Budget Grouping,Budget Category," \
                     "Natural Account,NAC desc"
        data_row = "Resource,Pay,Staff,51111001,Salaries"

        assert ArchivedNaturalCode.objects.all().count() == 0
        assert ArchivedExpenditureCategory.objects.all().count() == 0
        csvfile = [header_row, data_row]
        import_archived_nac(csvfile, 2019)
        assert ArchivedNaturalCode.objects.all().count() == 1
        assert ArchivedExpenditureCategory.objects.all().count() == 1

    def test_wrong_year(self):
        header_row = "Expenditure Type,Budget Grouping,Budget Category," \
                     "Natural Account,NAC desc"
        data_row = "Resource,Pay,Staff,51111001,Salaries"

        assert ArchivedNaturalCode.objects.all().count() == 0
        assert ArchivedExpenditureCategory.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(ArchiveYearError):
            import_archived_nac(csvfile, 2000)
        assert ArchivedNaturalCode.objects.all().count() == 0
        assert ArchivedExpenditureCategory.objects.all().count() == 0

    def test_wrong_header(self):
        header_row = "Expenditure Type,Budget Grouping,Budget Category," \
                     "NAC,NAC desc"
        data_row = "Resource,Pay,Staff,51111001,Salaries"

        assert ArchivedNaturalCode.objects.all().count() == 0
        assert ArchivedExpenditureCategory.objects.all().count() == 0
        csvfile = [header_row, data_row]
        with self.assertRaises(WrongChartOFAccountCodeException):
            import_archived_nac(csvfile, 2019)
        assert ArchivedNaturalCode.objects.all().count() == 0
        assert ArchivedExpenditureCategory.objects.all().count() == 0
