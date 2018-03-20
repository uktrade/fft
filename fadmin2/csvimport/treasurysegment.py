from core.models import SubSegments, Segments, SegmentParents, SegmentGrandParents, EstimateRows, SegmentGrandParents

import csv

# define the column position in the csv file.

COLUMN_KEY = {
    'Segment Department Code': 1,
    'Segment Department Long Name': 2,
    'Segment Grand Parent Code': 3,
    'Segment Grand Parent Long Name': 4,
    'Segment Parent Code': 5,
    'Segment Parent Long Name': 6,
    'Segment Code': 7,
    'Segment Long Name': 8,
    'Sub Segment Code': 9,
    'Sub Segment Long Name': 10,
    'COFOG L0 Code': 11,
    'COFOG L0 Long Name': 12,
    'COFOG L1 Code': 13,
    'COFOG L1 Long Name': 14,
    'COFOG L2 Code': 15,
    'COFOG L2 Long Name': 16,
    'Sub Function Code': 17,
    'Sub Function Long Name': 18,
    'Function Code': 19,
    'Function Long Name': 20,
    'Control Budget Code': 21,
    'Control Budget Long Name': 22,
    'Control Budget Detail Code': 23,
    'Coverage Code': 24,
    'Estimates Row Sort Order': 25,
    'Estimates Row Code': 26,
    'Estimates Row Long Name': 27,
    'Net Subhead Code': 28,
    'Policy Ringfence Code': 29,
    'Accounting Authority Code': 30,
    'Accounting Authority Detail Code': 31,
    'PESA 1.1 Code': 32,
    'PESA LA Grants Code': 33,
    'PESA LG Code': 34,
    'PESA Services Code': 35,
    'PESA Regional Code': 36
}


def import_treasury_segments(path):
    csvfile = open(path, newline='', encoding='cp1252')  # Windows-1252 or CP-1252, used because of a back quote
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        # Create Segment Hierarchy
        obj_segment_gp, created = SegmentGrandParents.objects.get_or_create(
            SegmentGrandParentCode=row[COLUMN_KEY['Segment Grand Parent Code']],
            SegmentGrandParentLongName=row[COLUMN_KEY['Segment Grand Parent Long Name']]
        )
        obj_segment_parent, created = SegmentParents.objects.get_or_create(
            SegmentGrandParentCode=obj_segment_gp,
            SegmentParentCode=row[COLUMN_KEY['Segment Parent Code']],
            SegmentParentLongName=row[COLUMN_KEY['Segment Parent Long Name']]
        )
        obj_segment, created = Segments.objects.get_or_create(
            SegmentParentCode=obj_segment_parent,
            SegmentCode=row[COLUMN_KEY['Segment Code']],
            SegmentLongName=row[COLUMN_KEY['Segment Long Name']]
        )
        obj_er, created = EstimateRows.objects.get_or_create(
            EstimatesRowCode=row[COLUMN_KEY['Estimates Row Code']],
            EstimatesRowLongName=row[COLUMN_KEY['Estimates Row Long Name']]
        )
        obj_subsegment, created = SubSegments.objects.get_or_create(
            SegmentCode=obj_segment,
            SubSegmentCode=row[COLUMN_KEY['Sub Segment Code']],
            SubSegmentLongName=row[COLUMN_KEY['Sub Segment Long Name']],
            EstimatesRowCode=obj_er
        )

