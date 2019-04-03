
from core.archive import archive_generic
from .models import ProjectCode, HistoricalProjectCode, ProgrammeCode, HistoricalProgrammeCode, \
    HistoricalExpenditureCategory, ExpenditureCategory, HistoricalInterEntity,  InterEntity, \
    HistoricalFCOMapping, FCOMapping,  HistoricalCommercialCategory, CommercialCategory, \
    HistoricalAnalysis1, Analysis1, HistoricalAnalysis2, Analysis2


def archive_project_code(year):
    archive_generic(year, HistoricalProjectCode, ProjectCode)


def archive_programme_code(year):
    archive_generic(year, HistoricalProgrammeCode, ProgrammeCode)


def archive_expenditure_category(year):
    archive_generic(year, HistoricalExpenditureCategory, ExpenditureCategory)


def archive_inter_entity(year):
    archive_generic(year, HistoricalInterEntity, InterEntity)


def archive_fco_mapping(year):
    archive_generic(year, HistoricalFCOMapping, FCOMapping)


def archive_commercial_category(year):
    archive_generic(year, HistoricalCommercialCategory, CommercialCategory)


def archive_analysis_1(year):
    archive_generic(year, HistoricalAnalysis1, Analysis1)


def archive_analysis_2(year):
    archive_generic(year, HistoricalAnalysis2, Analysis2)


