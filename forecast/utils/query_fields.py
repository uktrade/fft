
from chartofaccountDIT.models import (ArchivedExpenditureCategory,
                                      ArchivedProgrammeCode,
                                      ArchivedProjectCode,
                                      ExpenditureCategory,
                                      ProgrammeCode,
                                      ProjectCode)

from core.utils.generic_helpers import get_current_financial_year

from costcentre.models import (ArchivedCostCentre,
                               CostCentre,
                               DepartmentalGroup,
                               Directorate,
                               )


from end_of_month.models import forecast_budget_view_model

from previous_years.models import ArchivedForecastData

financial_code_prefix = "financial_code__"
SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3


class ForecastQueryFields:
    # This massive class handles the difference in the tables and field name
    # between the current chart of account and the archived ones.    #
    # This class return the correct field using 'current' to decide
    # what to return.
    def __init__(self, period=0):
        # period : between 0 and 15 it refers to the current financial year,
        # otherwise it contains the archived year to be used.
        self.current_year = period < 2000
        self.period = period
        self._datamodel = None
        if self.current_year:
            self.selected_year = get_current_financial_year()
        else:
            self.selected_year = period

    financial_code_prefix = "financial_code__"
    # indicates if DEL, AME, ADMIN
    budget_type_field = (
        f"{financial_code_prefix}programme__budget_type__budget_type_display"
    )
    budget_type_order_field = f"{financial_code_prefix}programme__budget_type__budget_type_display_order"  # noqa
    budget_type_edit_order_field = f"{financial_code_prefix}programme__budget_type__budget_type_edit_display_order"  # noqa

    # Categories defined by DIT: i.e. Consultancy, Contingency, Contractors, etc
    budget_category_id_field = (
        f"{financial_code_prefix}natural_account_code__expenditure_category__id"
    )

    budget_category_name_field = f"{financial_code_prefix}natural_account_code__expenditure_category__grouping_description"  # noqa
    budget_category_order_field = f"{financial_code_prefix}natural_account_code__expenditure_category__expenditurecategory_display_order"  # noqa

    # PAY, NON-PAY, CAPITAL, NON-CASH
    budget_grouping_field = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_description"  # noqa
    budget_grouping_order_field = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_display_order"  # noqa
    budget_nac_field = f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code"  # noqa

    @property
    def budget_nac_description_field(self):
        if self.current_year:
            return f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code__natural_account_code_description"  # noqa
        return f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code_description"  # noqa

    # Admin, Capital or Programme
    expenditure_type_name_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_name"  # noqa
    expenditure_type_description_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_description"  # noqa
    expenditure_type_order_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_display_order"  # noqa

    programme_code_field = f"{financial_code_prefix}programme__programme_code"
    programme_name_field = f"{financial_code_prefix}programme__programme_description"

    @property
    def cost_centre_name_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__cost_centre_name"
        return f"{financial_code_prefix}cost_centre__cost_centre_name"

    @property
    def cost_centre_code_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__cost_centre_code"
        return f"{financial_code_prefix}cost_centre__cost_centre_code"

    @property
    def directorate_name_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__directorate__directorate_name"
        return f"{financial_code_prefix}cost_centre__directorate_name"

    @property
    def directorate_code_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__directorate__directorate_code"
        return f"{financial_code_prefix}cost_centre__directorate_code"

    @property
    def group_name_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__directorate__group__group_name"
        return f"{financial_code_prefix}cost_centre__group_name"

    @property
    def group_code_field(self):
        if self.current_year:
            return f"{financial_code_prefix}cost_centre__directorate__group__group_code"
        return f"{financial_code_prefix}cost_centre__group_code"

    nac_code_field = (
        f"{financial_code_prefix}natural_account_code__natural_account_code"
    )
    nac_name_field = f"{financial_code_prefix}natural_account_code__natural_account_code_description"  # noqa
    nac_expenditure_type_field = (
        f"{financial_code_prefix}natural_account_code__economic_budget_code"  # noqa
    )

    project_code_field = f"{financial_code_prefix}project_code__project_code"
    project_name_field = f"{financial_code_prefix}project_code__project_description"

    analysis1_code_field = f"{financial_code_prefix}analysis1_code__analysis1_code"
    analysis1_name_field = (
        f"{financial_code_prefix}analysis1_code__analysis1_description"
    )

    analysis2_code_field = f"{financial_code_prefix}analysis2_code__analysis2_code"
    analysis2_name_field = (
        f"{financial_code_prefix}analysis2_code__analysis2_description"
    )

    @property
    def cost_centre_columns(self):
        return {
            self.budget_type_field: "Budget type",
            self.cost_centre_name_field: "Cost Centre description",
            self.cost_centre_code_field: "code",
        }

    @property
    def directorate_columns(self):
        return {
            self.budget_type_field: "Budget Type",
            self.directorate_name_field: "Directorate description",
            self.directorate_code_field: "code",
        }

    @property
    def group_columns(self):
        return {
            self.budget_type_field: "Budget Type",
            self.group_name_field: "Departmental Group description",
            self.group_code_field: "code",
        }

    @property
    def hierarchy_sub_total(self):
        return [self.budget_type_field]

    @property
    def programme_columns(self):
        return {
            self.budget_type_field: "Hidden",
            self.expenditure_type_description_field: "Hidden",
            self.expenditure_type_name_field: "Expenditure type",
            self.programme_name_field: "Programme code",
            self.programme_code_field: "code",
        }

    @property
    def programme_order_list(self):
        return [
            self.budget_type_order_field,
            self.expenditure_type_order_field,
        ]

    @property
    def programme_sub_total(self):
        return [
            self.budget_type_field,
            self.expenditure_type_description_field,
        ]

    @property
    def programme_display_sub_total_column(self):
        return self.programme_name_field

    @property
    def programme_detail_view(self):
        list = [
            "programme_details_dit",
            "programme_details_group",
            "programme_details_directorate",
        ]
        return list[self.hierarchy_type]

    # Expenditure data
    @property
    def expenditure_columns(self):
        return {
            self.budget_type_field: "Hidden",
            self.budget_category_id_field: "Hidden",
            self.budget_grouping_field: "Budget grouping",
            self.budget_category_name_field: "Budget category",
        }

    @property
    def expenditure_sub_total(self):
        return [
            self.budget_type_field,
            self.budget_grouping_field,
        ]

    @property
    def expenditure_display_sub_total_column(self):
        return self.budget_category_name_field

    @property
    def expenditure_order_list(self):
        return [
            self.budget_type_order_field,
            self.budget_grouping_order_field,
            self.budget_category_order_field,
        ]

    # Project data
    @property
    def project_columns(self):
        return {
            self.project_name_field: "Project",
            self.project_code_field: "code",
            self.expenditure_type_order_field: "Hidden",
            self.expenditure_type_name_field: "Expenditure type",
        }

    @property
    def project_order_list(self):
        return [
            self.project_code_field,
            self.expenditure_type_order_field,
        ]

    @property
    def project_sub_total(self):
        return [
            self.project_name_field,
        ]

    @property
    def project_display_sub_total_column(self):
        return self.project_code_field

    @property
    def project_detail_view(self):
        list = [
            "project_details_dit",
            "project_details_group",
            "project_details_directorate",
            "project_details_costcentre",
        ]
        return list[self.hierarchy_type]

    @property
    def filter_codes(self):
        list = ["", "group_code", "directorate_code", "cost_centre_code"]
        return list[self.hierarchy_type]

    @property
    def filter_selector(self):
        list = [
            "",
            self.group_code_field,
            self.directorate_code_field,
            self.cost_centre_code_field,
        ]
        return list[self.hierarchy_type]

    @property
    def hierarchy_columns(self):
        list = [
            self.group_columns,
            self.directorate_columns,
            self.cost_centre_columns,
            self.cost_centre_columns,
        ]
        return list[self.hierarchy_type]

    @property
    def hierarchy_sub_total_column(self):
        list = [
            self.group_name_field,
            self.directorate_name_field,
            self.cost_centre_name_field,
            self.cost_centre_name_field,
        ]
        return list[self.hierarchy_type]

    @property
    def hierarchy_order_list(self):
        list = [
            [self.budget_type_order_field, self.group_name_field, ],
            [self.budget_type_order_field, self.directorate_name_field, ],
            [self.budget_type_order_field, self.cost_centre_name_field, ],
            [self.budget_type_order_field, ],
        ]
        return list[self.hierarchy_type]

    @property
    def hierarchy_view_link_column(self):
        list = [
            self.group_name_field,
            self.directorate_name_field,
            self.cost_centre_name_field,
        ]
        return list[self.hierarchy_type]

    # view names used to display different level of forecast
    @property
    def hierarchy_view(self):
        list = ["forecast_group", "forecast_directorate", "forecast_cost_centre"]
        return list[self.hierarchy_type]

    @property
    def hierarchy_view_code(self):
        list = [
            self.group_code_field,
            self.directorate_code_field,
            self.cost_centre_code_field,
        ]
        return list[self.hierarchy_type]

    @property
    def expenditure_view(self):
        list = [
            "expenditure_details_dit",
            "expenditure_details_group",
            "expenditure_details_directorate",
            "expenditure_details_cost_centre",
        ]
        return list[self.hierarchy_type]

    # NAC data
    @property
    def nac_columns(self):
        return {
            self.budget_category_name_field: "Hidden",
            self.nac_name_field: "Natural Account code",
            self.nac_code_field: "code",
        }

    @property
    def nac_sub_total(self):
        return [
            self.budget_category_name_field,
        ]

    @property
    def nac_display_sub_total_column(self):
        return self.nac_name_field

    @property
    def nac_order_list(self):
        return [
            self.nac_name_field,
        ]

    # programme details data
    @property
    def programme_details_dit_columns(self):
        return {
            self.programme_name_field: "Hidden",
            self.expenditure_type_name_field: "Expenditure type",
            self.group_name_field: "Departmental Group",
            self.group_code_field: "code",
        }

    @property
    def programme_details_group_columns(self):
        return {
            self.programme_name_field: "Hidden",
            self.expenditure_type_name_field: "Expenditure type",
            self.directorate_name_field: "Directorate",
            self.directorate_code_field: "code",
        }

    @property
    def programme_details_directorate_columns(self):
        return {
            self.programme_name_field: "Hidden",
            self.expenditure_type_name_field: "Expenditure type",
            self.cost_centre_name_field: "Cost Centre",
            self.cost_centre_code_field: "code",
        }

    @property
    def programme_details_sub_total(self):
        return [
            self.programme_name_field,
        ]

    @property
    def programme_details_display_sub_total_column(self):
        return self.expenditure_type_name_field

    @property
    def programme_details_dit_order_list(self):
        return [
            self.group_name_field,
        ]

    @property
    def programme_details_group_order_list(self):
        return [
            self.directorate_name_field,
        ]

    @property
    def programme_details_directorate_order_list(self):
        return [
            self.cost_centre_name_field,
        ]

    @property
    def programme_details_hierarchy_order_list(self):
        list = [
            self.programme_details_dit_order_list,
            self.programme_details_group_order_list,
            self.programme_details_directorate_order_list,
            "",
        ]
        return list[self.hierarchy_type]

    @property
    def programme_details_hierarchy_columns(self):
        list = [
            self.programme_details_dit_columns,
            self.programme_details_group_columns,
            self.programme_details_directorate_columns,
            "",
        ]
        return list[self.hierarchy_type]

    @property
    def programme_details_hierarchy_sub_total_column(self):
        list = [
            self.group_name_field,
            self.directorate_name_field,
            self.cost_centre_name_field,
            "",
        ]
        return list[self.hierarchy_type]

    # Project details views
    @property
    def project_details_dit_columns(self):
        return {
            self.expenditure_type_name_field: "Expenditure type",
            self.group_name_field: "Departmental Group",
            self.group_code_field: "code",
        }

    @property
    def project_details_group_columns(self):
        return {
            self.expenditure_type_name_field: "Expenditure type",
            self.directorate_name_field: "Directorate",
            self.directorate_code_field: "code",
        }

    @property
    def project_details_directorate_columns(self):
        return {
            self.expenditure_type_name_field: "Expenditure type",
            self.cost_centre_name_field: "Cost Centre",
            self.cost_centre_code_field: "code",
        }

    @property
    def project_details_costcentre_columns(self):
        return {
            self.expenditure_type_name_field: "Expenditure type",
            self.cost_centre_name_field: "Cost Centre",
            self.cost_centre_code_field: "code",
        }

    @property
    def project_details_sub_total(self):
        return [
            self.expenditure_type_name_field,
        ]

    @property
    def project_details_dit_order_list(self):
        return [
            self.group_name_field,
            self.expenditure_type_name_field,
        ]

    @property
    def project_details_group_order_list(self):
        return [
            self.directorate_name_field,
            self.expenditure_type_name_field,
        ]

    @property
    def project_details_directorate_order_list(self):
        return [
            self.cost_centre_name_field,
            self.expenditure_type_name_field,
        ]

    @property
    def project_details_costcentre_order_list(self):
        return [
            self.expenditure_type_name_field,
        ]

    @property
    def project_details_hierarchy_order_list(self):
        list = [
            self.project_details_dit_order_list,
            self.project_details_group_order_list,
            self.project_details_directorate_order_list,
            self.project_details_costcentre_order_list,
        ]
        return list[self.hierarchy_type]

    @property
    def project_details_hierarchy_columns(self):
        list = [
            self.project_details_dit_columns,
            self.project_details_group_columns,
            self.project_details_directorate_columns,
            self.project_details_costcentre_columns,
        ]
        return list[self.hierarchy_type]

    @property
    def project_details_hierarchy_sub_total_column(self):
        list = [
            self.group_name_field,
            self.directorate_name_field,
            self.cost_centre_name_field,
            self.cost_centre_name_field,
        ]
        return list[self.hierarchy_type]

    @property
    def DEFAULT_PIVOT_COLUMNS(self):
        return {
            self.cost_centre_code_field: "Cost Centre code",
            self.cost_centre_name_field: "Cost Centre description",
            self.nac_code_field: "Natural Account code",
            self.nac_name_field: "Natural Account code description",
            self.programme_code_field: "Programme code",
            self.programme_name_field: "Programme code description",
            self.analysis1_code_field: "Contract code",
            self.analysis1_name_field: "Contract description",
            self.analysis2_code_field: "Market code",
            self.analysis2_name_field: "Market description",
            self.project_code_field: "Project code",
            self.project_name_field: "Project description",
        }

    @property
    def VIEW_FORECAST_DOWNLOAD_COLUMNS(self):
        return {
            self.group_name_field: "Group name",
            self.group_code_field: "Group code",
            self.directorate_name_field: "Directorate name",
            self.directorate_code_field: "Directorate code",
            self.cost_centre_name_field: "Cost Centre name",
            self.cost_centre_code_field: "Cost Centre code",
            self.budget_grouping_field: "Budget grouping",
            self.expenditure_type_name_field: "Expenditure type",
            self.expenditure_type_description_field: "Expenditure type description",
            self.budget_type_field: "Budget Type",
            self.budget_category_name_field: "Budget category",
            self.budget_nac_field: "Budget/Forecast NAC",
            self.budget_nac_description_field: "Budget/Forecast NAC description",
            self.nac_code_field: "PO/Actual NAC",
            self.nac_name_field: "Natural Account code description",
            self.nac_expenditure_type_field: "NAC Expenditure type",
            self.programme_code_field: "Programme code",
            self.programme_name_field: "Programme code description",
            self.analysis1_code_field: "Contract code",
            self.analysis1_name_field: "Contract description",
            self.analysis2_code_field: "Market code",
            self.analysis2_name_field: "Market description",
            self.project_code_field: "Project code",
            self.project_name_field: "Project description",
        }

    @property
    def EDIT_KEYS_DOWNLOAD(self):
        return {
            self.programme_code_field: "Programme code",
            self.programme_name_field: "Programme code Description",
            self.nac_code_field: "Natural Account code",
            self.nac_name_field: "Natural Account Code Description",
            self.analysis1_code_field: "Contract Code",
            self.analysis2_code_field: "Market Code",
            self.project_code_field: "Project Code",
        }

    @property
    def EDIT_FORECAST_DOWNLOAD_COLUMNS(self):
        return {
            self.group_name_field: "Group name",
            self.group_code_field: "Group code",
            self.directorate_name_field: "Directorate name",
            self.directorate_code_field: "Directorate code",
            self.cost_centre_name_field: "Cost Centre name",
            self.cost_centre_code_field: "Cost Centre code",
            self.budget_grouping_field: "Budget Grouping",
            self.expenditure_type_name_field: "Expenditure type",
            self.expenditure_type_description_field: "Expenditure type description",
            self.budget_type_field: "Budget type",
            self.budget_category_name_field: "Budget Category",
            self.budget_nac_field: "Budget/Forecast NAC",
            self.budget_nac_description_field: "Budget/Forecast NAC Description",
            self.nac_expenditure_type_field: "NAC Expenditure Type",
            self.analysis1_name_field: "Contract Description",
            self.analysis2_name_field: "Market Description",
            self.project_name_field: "Project Description",
        }

    @property
    def EDIT_FORECAST_DOWNLOAD_ORDER(self):
        return [
            self.budget_type_edit_order_field,
            self.programme_code_field,
            self.budget_grouping_order_field,
            self.nac_code_field,
        ]

    @property
    def MI_REPORT_DOWNLOAD_COLUMNS(self):
        return {
            self.cost_centre_code_field: "Cost Centre code",
            self.nac_code_field: "Natural Account code",
            self.programme_code_field: "Programme code",
            self.analysis1_code_field: "Contract Code",
            self.analysis2_code_field: "Market Code",
            self.project_code_field: "Project Code",
        }

    @property
    def datamodel(self):
        if self._datamodel is None:
            if self.current_year:
                self._datamodel = forecast_budget_view_model[self.period]
            else:
                self._datamodel = ArchivedForecastData
        return self._datamodel

    # The next methods return the correct objects (archived or not)
    # using the period to decide which one to use
    def group(self, group_code):
        if self.current_year:
            return DepartmentalGroup.objects.get(
                group_code=group_code
            )
        queryset = ArchivedCostCentre.objects.filter(
            group_code=group_code,
            financial_year_id=self.period,
        )
        return queryset.first()

    def directorate(self, directorate_code):
        if self.current_year:
            return Directorate.objects.get(
                directorate_code=directorate_code,
            )
        queryset = ArchivedCostCentre.objects.filter(
            directorate_code=directorate_code,
            financial_year_id=self.period,
        )
        return queryset.first()

    def cost_centre(self, cost_centre_code):
        if self.current_year:
            return CostCentre.objects.get(cost_centre_code=cost_centre_code, )
        queryset = ArchivedCostCentre.objects.filter(
            cost_centre_code=cost_centre_code,
            financial_year_id=self.period,
        )
        return queryset.first()

    def expenditure_category(self, expenditure_category_id):
        if self.current_year:
            return ExpenditureCategory.objects.get(pk=expenditure_category_id)
        return ArchivedExpenditureCategory.objects.get(pk=expenditure_category_id)

    def programme_code(self, programme_code):
        if self.current_year:
            return ProgrammeCode.objects.get(pk=programme_code)

        return ArchivedProgrammeCode.objects.get(
            programme_code=programme_code,
            financial_year_id=self.period,
        )

    def project_code(self, project_code):
        if self.current_year:
            return ProjectCode.objects.get(pk=project_code)

        return ArchivedProjectCode.objects.get(
            project_code=project_code,
            financial_year_id=self.period,
        )


def edit_forecast_order():
    # remove financial_code__ prefix from the
    # fields used in the download order.
    edit_fields = ForecastQueryFields()
    order_list = []
    prefix_len = len(financial_code_prefix)
    for elem in edit_fields.EDIT_FORECAST_DOWNLOAD_ORDER:
        order_list.append(elem[prefix_len:])
    return order_list
