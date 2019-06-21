import operator

from core.importcsv import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_MODEL_KEY, \
    IMPORT_CSV_PK_KEY, ImportInfo, import_obj

from .models import DITSSGroup, EstimateRow, Segment, SegmentGrandParent, SegmentParent, SubSegment

# Segment Department Code
# Segment Department Long Name
# Segment Grand Parent Code
# Segment Grand Parent Long Name
# Segment Parent Code
# Segment Parent Long Name
# Segment Code
# Segment Long Name
# Sub Segment Code
# Sub Segment Long Name
# COFOG L0 Code
# COFOG L0 Long Name
# COFOG L1 Code
# COFOG L1 Long Name
# COFOG L2 Code
# COFOG L2 Long Name
# Sub Function Code
# Sub Function Long Name
# Function Code
# Function Long Name
# Control Budget Code
# Control Budget Long Name
# Control Budget Detail Code
# Coverage Code
# Estimates Row Sort Order
# Estimates Row Code
# Estimates Row Long Name
# Net Subhead Code
# Policy Ringfence Code
# Accounting Authority Code
# Accounting Authority Detail Code
# PESA 1.1 Code
# PESA LA Grants Code
# PESA LG Code
# PESA Services Code
# PESA Regional Code


# noqa: E501 tells Flake8 to ignore lines that are to long
SEGMENT_GP_KEY = {IMPORT_CSV_MODEL_KEY: SegmentGrandParent,
          IMPORT_CSV_PK_KEY: 'Segment Grand Parent Code',
          IMPORT_CSV_FIELDLIST_KEY: {SegmentGrandParent.segment_grand_parent_long_name.field_name: 'Segment Grand Parent Long Name',  # noqa: E501
                                     SegmentGrandParent.segment_department_code.field_name: 'Segment Department Code',
                                     SegmentGrandParent.segment_department_long_name.field_name: 'Segment Department Long Name'}}

SEGMENT_P_KEY = {IMPORT_CSV_MODEL_KEY: SegmentParent,
          IMPORT_CSV_PK_KEY: 'Segment Parent Code',
          IMPORT_CSV_FIELDLIST_KEY: {SegmentParent.segment_parent_long_name.field_name: 'Segment Parent Long Name',  # noqa: E501
                                     SegmentParent.segment_grand_parent_code.field.name: SEGMENT_GP_KEY}}



SEGMENT_KEY = {IMPORT_CSV_MODEL_KEY: Segment,
          IMPORT_CSV_PK_KEY: 'Segment Code',
          IMPORT_CSV_FIELDLIST_KEY: {Segment.segment_long_name.field_name: 'Segment Long Name',  # noqa: E501
                                     Segment.segment_parent_code.field.name: SEGMENT_P_KEY}}


ESTIMATE_ROW_KEY = {IMPORT_CSV_MODEL_KEY: EstimateRow,
          IMPORT_CSV_PK_KEY: 'Estimates Row Code',
          IMPORT_CSV_FIELDLIST_KEY: {EstimateRow.estimate_row_long_name.field_name: 'Estimates Row Long Name'} } # noqa: E501


SUB_SEGMENT_KEY = {IMPORT_CSV_MODEL_KEY: SubSegment,
          IMPORT_CSV_PK_KEY: 'Sub Segment Code',
          IMPORT_CSV_FIELDLIST_KEY: {'sub_segment_long_name': 'Segment Long Name',  # noqa: E501
                                     SubSegment.Segment_code.field.name: SEGMENT_KEY,
                                     'control_budget_detail_code': 'Control Budget Detail Code',
                                     SubSegment.estimates_row_code.field.name: ESTIMATE_ROW_KEY,
                                     SubSegment.accounting_authority_code.field_name: 'Accounting Authority Code',
                                     SubSegment.accounting_authority_DetailCode.field_name: 'Accounting Authority Detail Code'
                                     }}

def import_treasury_SS(csvfile):
    import_obj(csvfile, SUB_SEGMENT_KEY, operator.eq, 'Segment Department Code', 'UKT013.GROUP')


import_SS_class = ImportInfo(SUB_SEGMENT_KEY, 'OSCAR Sub-Segments', filter=[operator.eq, 'Segment Department Code', 'UKT013.GROUP'])