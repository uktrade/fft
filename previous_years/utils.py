from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year

from costcentre.models import ArchivedCostCentre

from forecast.utils.import_helpers import CheckFinancialCode

from previous_years.models import ArchivedFinancialCode


class CheckArchivedFinancialCode(CheckFinancialCode):
    """Uses the logic in CheckFinancialCode, but extract
    the chart of account from the archived tables"""

    def __init__(self, financial_year, file_upload):
        self.cost_centre_model = ArchivedCostCentre
        self.programme_code_model = ArchivedProgrammeCode
        self.analysis1_model = ArchivedAnalysis1
        self.analysis2_model = ArchivedAnalysis2
        self.project_code_model = ArchivedProjectCode
        self.natural_code_model = ArchivedNaturalCode
        self.financial_year = financial_year
        super().__init__(file_upload)

    def get_chart_of_account_object(self, m, value):
        msg = ""
        try:
            field_name = m.chart_of_account_code_name
            kwargs = {}
            kwargs[field_name] = value
            kwargs["financial_year_id"] = self.financial_year
            obj = m.objects.get(**kwargs)
        except m.DoesNotExist:
            msg = f'{field_name} "{value}" does not exist.\n'
            obj = None
        except ValueError:
            msg = f'{field_name} "{value}" is the wrong type.\n'
            obj = None
        return obj, msg

    def get_info_tuple(self, model, pk, make_active=True):
        status = self.IGNORE
        obj, msg = self.get_chart_of_account_object(model, pk)
        if not obj:
            status = self.CODE_ERROR
        else:
            if obj.active:
                status = self.CODE_OK
                msg = ""
            else:
                if make_active:
                    obj.active = True
                    obj.save()
                    status = self.CODE_WARNING
                    msg = (
                        f'{(model.chart_of_account_code_name)} "{pk}" '
                        f"added to the approved list. \n"
                    )
        info_tuple = (obj, status, msg)
        return info_tuple

    def get_financial_code(self):
        if self.error_found:
            return None
        financial_code_obj, created = ArchivedFinancialCode.objects.get_or_create(
            programme=self.programme_obj,
            cost_centre=self.cc_obj,
            natural_account_code=self.nac_obj,
            analysis1_code=self.analysis1_obj,
            analysis2_code=self.analysis2_obj,
            project_code=self.project_obj,
            financial_year_id=self.financial_year,
        )
        financial_code_obj.save()
        return financial_code_obj


class ArchiveYearError(Exception):
    pass


def validate_year_for_archiving(financial_year):
    current_year = get_current_financial_year()
    if financial_year == current_year:
        raise (ArchiveYearError(f"{financial_year} is the current year."))

    if financial_year == current_year:
        raise (ArchiveYearError(f"{financial_year} is in the future."))

    try:
        obj = FinancialYear.objects.get(pk=financial_year)
    except FinancialYear.DoesNotExist:
        raise (ArchiveYearError(f"Financial year {financial_year} does not exist."))
    return obj


def validate_year_for_archiving_actuals(financial_year):
    obj = validate_year_for_archiving(financial_year)

    # Checks if there are cost centres archived for this year
    # and all the mandatory members of the Chart of Account
    # check that the chart of account has been archived.
    # otherwise, every single row of the uploaded file will generate an error
    error_found = False
    error_msg = ""
    if obj.costcentre_archivedcostcentre.all().count() == 0:
        error_found = True
        error_msg = "No cost centres available. "

    if obj.chartofaccountdit_archivednaturalcode.all().count() == 0:
        error_found = True
        error_msg = f"{error_msg}No natural account code available. "

    if obj.chartofaccountdit_archivedprogrammecode.all().count() == 0:
        error_found = True
        error_msg = f"{error_msg}No programme code available. "

    if error_found:
        raise (
            ArchiveYearError(
                f"Error(s) in chart of account for {financial_year}: f{error_msg}"
            )
        )
