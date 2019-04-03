
from core.archive import archive_generic
from .models import ProjectCode, HistoricalProjectCode, ProgrammeCode, HistoricalProgrammeCode, \
    HistoricalExpenditureCategory, ExpenditureCategory, HistoricalInterEntity,  InterEntity


def archive_project_code(year):
    archive_generic(year, HistoricalProjectCode, ProjectCode)


def archive_programme_code(year):
    archive_generic(year, HistoricalProgrammeCode, ProgrammeCode)


def archive_expenditure_category(year):
    archive_generic(year, HistoricalExpenditureCategory, ExpenditureCategory)

def archive_inter_entity(year):
    archive_generic(year, HistoricalInterEntity, InterEntity)
