import csv

from core.importcsv import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_IS_FK, IMPORT_CSV_MODEL_KEY, \
    IMPORT_CSV_PK_KEY, IMPORT_CSV_PK_NAME_KEY, ImportInfo, \
    import_list_obj, import_obj

from .models import  GiftAndHospitalityCompany, \
    GiftAndHospitalityCategory, GiftAndHospitalityClassification


GH_CLASSIF_KEY = {IMPORT_CSV_MODEL_KEY: GiftAndHospitalityClassification,
                    IMPORT_CSV_PK_NAME_KEY:
                        GiftAndHospitalityClassification.gif_hospitality_classification.field_name,
                    IMPORT_CSV_PK_KEY: 'Classification',
                    IMPORT_CSV_FIELDLIST_KEY: {
                        GiftAndHospitalityClassification.gift_type.field_name: 'Type',
                 }}

import_gh_classification_class = ImportInfo(GH_CLASSIF_KEY)


GH_COMPANY_KEY = {IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCompany,
                    IMPORT_CSV_PK_KEY: 'Company',
                    IMPORT_CSV_PK_NAME_KEY:
                            GiftAndHospitalityCompany.gif_hospitality_company.field_name,
                    IMPORT_CSV_FIELDLIST_KEY: {}}

import_gh_company_class = ImportInfo(GH_COMPANY_KEY)


GH_CATEGORY_KEY = {IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCategory,
                    IMPORT_CSV_PK_KEY: 'Category',
                    IMPORT_CSV_PK_NAME_KEY:
                       GiftAndHospitalityCategory.gif_hospitality_category.field_name,
                    IMPORT_CSV_FIELDLIST_KEY: {}}

import_gh_category_class = ImportInfo(GH_CATEGORY_KEY)






