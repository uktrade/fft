from core.utils import today_string
from core.views import FAdminFilteredView

from .filters import Analysis1Filter, Analysis2Filter, \
    CommercialCategoryFilter, ExpenditureCategoryFilter, \
    InterEntityFilter, NACFilter, ProgrammeFilter, ProjectFilter
from .tables import Analysis1Table, Analysis2Table, \
    CommercialCategoryTable, ExpenditureCategoryTable, \
    InterEntityTable, NaturalCodeTable, ProgrammeTable, ProjectTable


class FilteredNACListView(FAdminFilteredView):
    table_class = NaturalCodeTable
    model = table_class.Meta.model
    filterset_class = NACFilter
    export_name = 'Natural Account Codes' + today_string()
    sheet_name = 'Natural Account Codes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Natural Account Codes (NAC)'
        context['section_description'] = 'This field tells us what we are ' \
                                         'spending the money on. ' \
                                         'The structure follows the Treasury Common Chart of ' \
                                         'Accounts and groups a set of transactions ' \
                                         'into a clearly defined category.'
        return context


class FilteredExpenditureCategoryListView(FAdminFilteredView):
    table_class = ExpenditureCategoryTable
    model = table_class.Meta.model
    filterset_class = ExpenditureCategoryFilter
    export_name = 'Budget Categories ' + today_string()
    sheet_name = 'Budget Categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Budget Categories'
        context['section_description'] = 'This field helps you in acquiring the correct ' \
                                         'Natural Account Code for your purchase ' \
                                         'from a financial perspective.'
        return context


class FilteredCommercialCategoryListView(FAdminFilteredView):
    table_class = CommercialCategoryTable
    model = table_class.Meta.model
    filterset_class = CommercialCategoryFilter
    export_name = 'Commercial Categories ' + today_string()
    sheet_name = 'Commercial Categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Commercial Categories'
        context['section_description'] = 'This field helps you in acquiring the correct ' \
                                         'Natural Account Code for your purchase ' \
                                         'from a procurement perspective.'
        return context


class FilteredAnalysis1ListView(FAdminFilteredView):
    table_class = Analysis1Table
    model = table_class.Meta.model
    filterset_class = Analysis1Filter
    export_name = 'Contract Reconciliation (Analysis 1) ' + today_string()
    sheet_name = 'Contract Reconciliation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Contract Reconciliation (Analysis 1)'
        context['section_description'] = 'This field helps to ' \
                                         'reconcile with Commercial’s unique ' \
                                         'contract identifier. It will enable the organisation ' \
                                         'to match spend on the financial system ' \
                                         'to specific contracts.'
        return context


class FilteredAnalysis2ListView(FAdminFilteredView):
    table_class = Analysis2Table
    model = table_class.Meta.model
    filterset_class = Analysis2Filter
    export_name = 'Markets (Analysis 2) ' + today_string()
    sheet_name = 'Markets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Markets (Analysis 2)'
        context['section_description'] = 'This field is used by the Overseas Team. ' \
                                         'The cost centre structure  identifies our 9 regions, ' \
                                         'however, within each region ' \
                                         'the spend is needed by country.'
        return context


class FilteredProgrammeView(FAdminFilteredView):
    table_class = ProgrammeTable
    model = table_class.Meta.model
    filterset_class = ProgrammeFilter
    export_name = 'Programme Codes ' + today_string()
    sheet_name = 'Programme Codes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Programme Codes'
        context['section_description'] = 'This field tells us why we are spending the money ' \
                                         'i.e. what we are trying to deliver on. ' \
                                         'This reflects the two most important reporting ' \
                                         'requirements that DIT is likely to have to HMG over ' \
                                         'the next few years (EU exit and ODA) ' \
                                         'and Parliament Control Total ' \
                                         '(DEL/AME and Admin/Programme).'
        return context


class FilteredInterEntityView(FAdminFilteredView):
    table_class = InterEntityTable
    model = table_class.Meta.model
    filterset_class = InterEntityFilter
    export_name = 'EntityInterEntity ' + today_string()
    sheet_name = 'EntityInterEntity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Entity-Inter Entity'
        context['section_description'] = 'This field is used to identify transactions with ' \
                                         'Other Government Departments (OGDs) / Bodies which ' \
                                         'is needed for the year-end accounts. To be used ' \
                                         'when setting up Purchase Orders and / or ' \
                                         'journals with OGDs.'
        return context


class FilteredProjectView(FAdminFilteredView):
    table_class = ProjectTable
    model = table_class.Meta.model
    filterset_class = ProjectFilter
    export_name = 'Project Codes ' + today_string()
    sheet_name = 'Project Codes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Project (Spare 1)'
        context['section_description'] = 'This field helps to identify DITs project / portfolio ' \
                                         'and report against them regardless where in the ' \
                                         'organisation expenditure is taking place i.e. ' \
                                         'Trade Remedies Authority (project) ' \
                                         'expenditure in TPG, ' \
                                         'Digital and Estates.'
        return context
