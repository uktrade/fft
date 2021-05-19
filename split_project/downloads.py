from core.utils.export_helpers import export_to_excel

from forecast.models import FinancialPeriod
from forecast.utils.export_helpers import get_obj_value

from split_project.import_project_percentage import (
    EXPECTED_PERCENTAGE_HEADERS,
    WORKSHEET_PROJECT_TITLE
)
from split_project.models import ProjectSplitCoefficient


def export_template(queryset):
    month_list = FinancialPeriod.financial_period_info.period_display_all_list()
    yield EXPECTED_PERCENTAGE_HEADERS + month_list


def create_template():
    return export_to_excel(None, export_template, WORKSHEET_PROJECT_TITLE)


def export_percentage(queryset, fields):
    month_list = FinancialPeriod.financial_period_info.period_display_all_list()
    yield list(
        fields.values()
    ) + month_list

    for obj in queryset:
        data_list = []
        for f in fields.keys():
            data_list.append(obj[f])
        for month in month_list:
            data_list.append(get_obj_value(obj, month) / 10000)
        yield data_list


def create_percentage_download():
    title = WORKSHEET_PROJECT_TITLE

    columns = {
        "financial_code_to__cost_centre__cost_centre_code":
            "Cost centre code",
        "financial_code_to__cost_centre__cost_centre_name":
            "Cost centre description",
        "financial_code_to__natural_account_code__natural_account_code":
            "Natural Account code",
        "financial_code_to__natural_account_code__natural_account_code_description":
            "Natural Account description",
        "financial_code_to__programme__programme_code":
            "Programme code",
        "financial_code_to__programme__programme_description":
            "Programme description",
        "financial_code_to__analysis1_code__analysis1_code":
            "Contract Code",
        "financial_code_to__analysis1_code__analysis1_description":
            "Contract description",
        "financial_code_to__analysis2_code__analysis2_code":
            "Market Code",
        "financial_code_to__analysis2_code__analysis2_description":
            "Market description",
        "financial_code_to__project_code__project_code":
            "Project Code",
        "financial_code_to__project_code__project_description":
            "Project description",
    }

    return export_to_excel(
        ProjectSplitCoefficient.pivot.pivot_data(columns),
        export_percentage,
        title,
        columns,
        "Percent",
    )
