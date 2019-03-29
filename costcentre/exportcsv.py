from core.exportutils import get_fk_value


def export_bp_iterator(queryset):
    yield ['Surname',
           'Name',
           'Email',
           'Active']
    for obj in queryset:
        yield [obj.surname,
               obj.name,
               obj.bp_email,
               obj.active]


def export_cc_iterator(queryset):
    yield ['Cost Centre', 'Cost Centre Description', 'Active', 'Disabled (Actuals to be cleared)',
           'Directorate', 'Directorate Description',
           'Group', 'Group Description',
           'BSCE Email']
    for obj in queryset:
        yield [int(obj.cost_centre_code),
               obj.cost_centre_name,
               obj.active,
               obj.disabled_with_actual,
               obj.directorate.directorate_code,
               obj.directorate.directorate_name,
               obj.directorate.group.group_code,
               obj.directorate.group.group_name,
               get_fk_value(obj.bsce_email, 'bsce_email')
               ]


def export_admin_cc_iterator(queryset):
    for obj in queryset:
        yield [1,
               '109TTT',
               'DIT',
               obj.directorate.group.group_code,
               obj.directorate.group.group_name,
               obj.directorate.directorate_code,
               obj.directorate.directorate_name,
               obj.cost_centre_code,
               obj.cost_centre_name,
               'Mentor Map',
               obj.active
               ]


def export_directorate_iterator(queryset):
    yield ['Directorate', 'Directorate Description', 'Active',
           'Group', 'Group Description', 'Group Active']
    for obj in queryset:
        yield [obj.directorate_code,
               obj.directorate_name,
               obj.active,
               obj.group.group_code,
               obj.group.group_name,
               obj.group.active]


def export_group_iterator(queryset):
    yield ['Group', 'Group Description', 'Active']
    for obj in queryset:
        yield [obj.group_code,
               obj.group_name,
               obj.active]


def export_bsce_iterator(queryset):
    yield ['BSCE Email', 'Active']
    for obj in queryset:
        yield [obj.bsce_email,
               obj.active]


def export_person_iterator(queryset):
    yield ['Surname',
           'Name',
           'Director General',
           'Director',
           'Active']
    for obj in queryset:
        yield [obj.surname,
               obj.name,
               obj.is_dg,
               obj.is_director,
               obj.active]


def export_historic_costcentre_iterator(queryset):
    yield ['Cost Centre', 'Cost Centre Description',
           'Deputy Director', 'Business Partner', 'BSCE Email'
           'Active', 'Disabled (Actuals to be cleared)',
           'Directorate', 'Directorate Description', 'Director'
           'Group', 'Group Description', 'Director General',
           'Financial Year', 'Date archived'
           ]
    for obj in queryset:
        yield [obj.cost_centre_code,
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
               obj.archived
               ]
