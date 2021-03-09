from core.archive import archive_generic

from .models import (
    Analysis1,
    Analysis2,
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)


def archive_project_code(year):
    return archive_generic(year, ArchivedProjectCode, ProjectCode)


def archive_programme_code(year):
    return archive_generic(year, ArchivedProgrammeCode, ProgrammeCode)


def archive_expenditure_category(year):
    return archive_generic(year, ArchivedExpenditureCategory, ExpenditureCategory)


def archive_inter_entity(year):
    return archive_generic(year, ArchivedInterEntity, InterEntity)


def archive_fco_mapping(year):
    return archive_generic(year, ArchivedFCOMapping, FCOMapping)


def archive_commercial_category(year):
    return archive_generic(year, ArchivedCommercialCategory, CommercialCategory)


def archive_analysis_1(year):
    return archive_generic(year, ArchivedAnalysis1, Analysis1)


def archive_analysis_2(year):
    return archive_generic(year, ArchivedAnalysis2, Analysis2)


def archive_natural_code(year):
    return archive_generic(year, ArchivedNaturalCode, NaturalCode)


def archive_all(year):
    # Delete the archived NAC first, otherwise they stop the deletion of
    # expenditure_category and commercial_category
    ArchivedNaturalCode.objects.filter(financial_year_id=year).delete()
    archive_project_code(year)
    archive_programme_code(year)
    archive_expenditure_category(year)
    archive_inter_entity(year)
    archive_fco_mapping(year)
    archive_commercial_category(year)
    archive_analysis_1(year)
    archive_analysis_2(year)
    archive_natural_code(year)
