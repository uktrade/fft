import csv

from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    ImportInfo,
    csv_header_to_dict,
    import_obj,
)

from .models import (
    BSCEEmail,
    BusinessPartner,
    CostCentre,
    CostCentrePerson,
    DepartmentalGroup,
    Directorate,
)

GROUP_KEY = {
    IMPORT_CSV_MODEL_KEY: DepartmentalGroup,
    IMPORT_CSV_PK_KEY: "Group Code",
    "fieldlist": {"group_name": "Group Description"},
}

DIR_KEY = {
    IMPORT_CSV_MODEL_KEY: Directorate,
    IMPORT_CSV_PK_KEY: "Directorate Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "directorate_name": "Directorate Description",
        "group": GROUP_KEY,
    },
}

CC_KEY = {
    IMPORT_CSV_MODEL_KEY: CostCentre,
    IMPORT_CSV_PK_KEY: "Cost Centre",
    IMPORT_CSV_FIELDLIST_KEY: {
        "cost_centre_name": "Cost Centre Description",
        "active": "Active",
        "directorate": DIR_KEY,
    },
}


def import_cc(csvfile):
    return import_obj(csvfile, CC_KEY)


import_cc_class = ImportInfo(
    CC_KEY, "Departmental Groups, Directorates and Cost Centres"
)


def get_field_from_row(row, header_name):
    temp = row[header_name]
    if temp:
        temp = temp.strip()
    else:
        temp = ''
    return temp


def import_cc_dit_specific(csvfile):
    """Special function to import the
    Deputy Director, Business partner
    and BSCE email"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csv_header_to_dict(next(reader))
    row_counter = 1
    for row in reader:
        row_counter += 1
        obj = CostCentre.objects.get(pk=row[header["cost centre"]].strip())
        deputy_name = get_field_from_row(row, header["deputy name"])
        deputy_surname = get_field_from_row(row, header["deputy surname"])
        if deputy_surname:
            deputy_obj, created = CostCentrePerson.objects.get_or_create(
                name=deputy_name,
                surname=deputy_surname,
            )
            deputy_obj.email = get_field_from_row(row, header["deputy email"])
            deputy_obj.active = True
            deputy_obj.save()
            obj.deputy_director = deputy_obj
        else:
            obj.deputy_director = None

        bp_name = get_field_from_row(row, header["bp name"])
        bp_surname = get_field_from_row(row, header["bp surname"])
        if bp_surname:
            bp_obj, created = BusinessPartner.objects.get_or_create(
                name=bp_name,
                surname=bp_surname,
            )
            bp_obj.bp_email = get_field_from_row(row, header["bp email"])
            bp_obj.active = True
            bp_obj.save()
            obj.business_partner = bp_obj
        else:
            obj.business_partner = None
        bsce_email = get_field_from_row(row, header["bsce email"])
        if bsce_email:
            bsce_obj, created = BSCEEmail.objects.get_or_create(
                bsce_email=bsce_email
            )
            obj.bsce_email = bsce_obj
        else:
            obj.bsce_email = None
        obj.save()
    return True, ""


import_cc_dit_specific_class = ImportInfo(
    {},
    "DIT Information",
    [
        "Cost Centre",
        "BP Name",
        "BP Surname",
        "BP Email",
        "Deputy Name",
        "Deputy Surname",
        "Deputy Email",
        "BSCE Email",
    ],
    import_cc_dit_specific,
)


def import_director(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csv_header_to_dict(next(reader))
    for row in reader:
        obj = Directorate.objects.get(pk=row[header["directorate code"]].strip())
        director_surname = get_field_from_row(row, header["director surname"])
        if director_surname:
            director_name = get_field_from_row(row, header["director name"])
            director_obj, created = CostCentrePerson.objects.get_or_create(
                name=director_name,
                surname=director_surname,
            )
            director_obj.email = get_field_from_row(row, header["director email"])
            director_obj.active = True
            director_obj.is_director = True
            director_obj.save()
        else:
            director_obj = None
        obj.director = director_obj
        obj.save()
    return True, ""


import_director_class = ImportInfo(
    {},
    "Directors",
    [
        "Directorate Code",
        "Director Name",
        "Director Surname",
        "Director Email",
    ],
    import_director,
)


def import_group_with_dg(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csv_header_to_dict(next(reader))
    for row in reader:
        dg_group = row[header["group code"]].strip()
        obj = DepartmentalGroup.objects.get(pk=dg_group)
        dg_obj, created = CostCentrePerson.objects.get_or_create(
            name=row[header["dg name"]].strip(),
            surname=row[header["dg surname"]].strip(),
        )
        dg_obj.email = row[header["dg email"]].strip()
        dg_obj.active = True
        dg_obj.is_dg = True
        dg_obj.save()
        obj.director_general = dg_obj
        obj.save()
    return True, ""


import_departmental_group_class = ImportInfo(
    {},
    "Director Generals",
    ["Group Code", "DG Name", "DG Surname", "DG email"],
    import_group_with_dg,
)
