from core.exportutils import get_fk_value


def export_bp_iterator(queryset):
    yield ["Surname", "Name", "Email", "Active"]
    for obj in queryset:
        yield [obj.surname, obj.name, obj.bp_email, obj.active]


def dd_field_obj(obj):
    if obj:
        return [obj.name, obj.surname, obj.email]
    else:
        return ["-", "-", "-"]


def bp_field_obj(obj):
    if obj:
        return [obj.name, obj.surname, obj.bp_email]
    else:
        return ["-", "-", "-"]


def export_cc_iterator(queryset):
    yield [
        "Cost Centre",
        "Cost Centre Description",
        "Directorate Code",
        "Directorate Description",
        "Group Code",
        "Group Description",
        "BSCE Email",
        "BP Name",
        "BP Surname",
        "BP Email",
        "Deputy Name",
        "Deputy Surname",
        "Deputy Email",
        "Active",
        "Used for Travel",
        "Disabled (Actuals to be cleared)",
        "Treasury Segment",
    ]
    for obj in queryset:
        yield [
            int(obj.cost_centre_code),
            obj.cost_centre_name,
            obj.directorate.directorate_code,
            obj.directorate.directorate_name,
            obj.directorate.group.group_code,
            obj.directorate.group.group_name,
            get_fk_value(obj.bsce_email, "bsce_email"),
        ] + bp_field_obj(obj.business_partner) + dd_field_obj(obj.deputy_director) + [
            obj.active,
            obj.used_for_travel,
            obj.disabled_with_actual,
            obj.directorate.group.treasury_segment_fk.segment_long_name
            if obj.directorate.group.treasury_segment_fk
            else "-",
        ]


def export_directorate_iterator(queryset):
    yield [
        "Directorate",
        "Directorate Description",
        "Active",
        "Group",
        "Group Description",
        "Group Active",
    ]
    for obj in queryset:
        yield [
            obj.directorate_code,
            obj.directorate_name,
            obj.active,
            obj.group.group_code,
            obj.group.group_name,
            obj.group.active,
        ]


def export_group_iterator(queryset):
    yield ["Group", "Group Description", "Treasury Segment", "Active"]
    for obj in queryset:
        yield [
            obj.group_code,
            obj.group_name,
            obj.treasury_segment_fk.segment_long_name
            if obj.treasury_segment_fk
            else "-",
            obj.active,
        ]


def export_bsce_iterator(queryset):
    yield ["BSCE Email", "Active"]
    for obj in queryset:
        yield [obj.bsce_email, obj.active]


def export_person_iterator(queryset):
    yield ["Surname", "Name", "Director General", "Director", "Active"]
    for obj in queryset:
        yield [obj.surname, obj.name, obj.is_dg, obj.is_director, obj.active]


def export_historic_costcentre_iterator(queryset):
    yield [
        "Cost Centre",
        "Cost Centre Description",
        "Deputy Director",
        "Business Partner",
        "BSCE Email",
        "Active",
        "Disabled (Actuals to be cleared)",
        "Directorate",
        "Directorate Description",
        "Director",
        "Group",
        "Group Description",
        "Director General",
        "Financial Year",
        "Date archived",
    ]
    for obj in queryset:
        yield [
            obj.cost_centre_code,
            obj.cost_centre_name,
            obj.deputy_director_fullname,
            obj.business_partner_fullname,
            obj.bsce_email,
            obj.active,
            obj.disabled_with_actual,
            obj.directorate_code,
            obj.directorate_name,
            obj.director_fullname,
            obj.group_code,
            obj.group_name,
            obj.dg_fullname,
            obj.financial_year.financial_year_display,
            obj.archived,
        ]
