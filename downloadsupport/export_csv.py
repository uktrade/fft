from chartofaccountDIT.models import NaturalCode

from core.exportutils import export_to_csv, get_fk_value

from costcentre.models import CostCentre


# The following is the expected list of fields for the query set
# 1,109TTT,DIT,1093HT,ITI - DG Office,10938T,CEO’s Office,109000,Chief Executive's Office,Mentor Map,Operations,Yes  # noqa
def export_cost_centre_iterator(queryset):
    for obj in queryset:
        yield [
            1,
            "109TTT",
            "DIT",
            get_fk_value(obj.directorate.group, "group_code"),
            get_fk_value(obj.directorate.group, "group_name"),
            get_fk_value(obj.directorate, "directorate_code"),
            get_fk_value(obj.directorate, "directorate_name"),
            obj.cost_centre_code,
            obj.cost_centre_name,
            "Mentor Map",
            "Operations",
            "Yes",
        ]


def export_cost_centres():
    queryset = CostCentre.objects.filter(active=True)
    return export_to_csv(queryset, export_cost_centre_iterator)


def alias_value(totest, value, alias):
    if totest == value:
        return alias
    else:
        return totest


def export_nac_hierarchy_iterator(queryset):
    for obj in queryset:
        yield [
            obj.natural_account_code,
            "Remove"
            if obj.expenditure_category is None
            else alias_value(
                get_fk_value(
                    obj.expenditure_category.NAC_category, "NAC_category_description"
                ),
                "Pay",
                "Staff Costs",
            ),
            get_fk_value(obj.expenditure_category, "grouping_description", "Remove"),
            obj.natural_account_code_description,
        ]


def export_nac_hierarchy():
    queryset = NaturalCode.objects.all()
    return export_to_csv(queryset, export_nac_hierarchy_iterator)


def export_nac_iterator(queryset):
    pass


def export_analysis1_iterator(queryset):
    pass


def export_analysis2_iterator(queryset):
    pass


def export_travel_cc_iterator(queryset):
    """Format requested by Trainline: dash between
    code and description,  max len is 30 chars"""
    for obj in queryset:
        yield ["{} - {}".format(obj.cost_centre_code, obj.cost_centre_name)[:30]]


def export_travel_cost_centres():
    queryset = CostCentre.objects.filter(active=True, used_for_travel=True)
    return export_to_csv(queryset, export_travel_cc_iterator)
