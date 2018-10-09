import csv

from treasurySS.models import EstimateRow, Segment, SegmentGrandParent, SegmentParent, SubSegment

# define the column position in the csv file.
COLUMN_KEY = {
    'Segment Department Code': 0,
    'Segment Department Long Name': 1,
    'Segment Grand Parent Code': 2,
    'Segment Grand Parent Long Name': 3,
    'Segment Parent Code': 4,
    'Segment Parent Long Name': 5,
    'Segment Code': 6,
    'Segment Long Name': 7,
    'Sub Segment Code': 8,
    'Sub Segment Long Name': 9,
    'COFOG L0 Code': 10,
    'COFOG L0 Long Name': 11,
    'COFOG L1 Code': 12,
    'COFOG L1 Long Name': 13,
    'COFOG L2 Code': 14,
    'COFOG L2 Long Name': 15,
    'Sub Function Code': 16,
    'Sub Function Long Name': 17,
    'Function Code': 18,
    'Function Long Name': 19,
    'Control Budget Code': 20,
    'Control Budget Long Name': 21,
    'Control Budget Detail Code': 22,
    'Coverage Code': 23,
    'Estimates Row Sort Order': 24,
    'Estimates Row Code': 25,
    'Estimates Row Long Name': 26,
    'Net Subhead Code': 27,
    'Policy Ringfence Code': 20,
    'Accounting Authority Code': 29,
    'Accounting Authority Detail Code': 30,
    'PESA 1.1 Code': 31,
    'PESA LA Grants Code': 32,
    'PESA LG Code': 33,
    'PESA Services Code': 34,
    'PESA Regional Code': 35
}


def import_treasury_segments(csvfile):
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    if has_header:
        next(reader)  # Skip header row.
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        if row[COLUMN_KEY['Segment Department Code']] == 'UKT013.GROUP':
            # Create Segment Hierarchy
            obj_segment_gp, created = SegmentGrandParent.objects.get_or_update(
                SegmentGrandParentCode=row[COLUMN_KEY['Segment Grand Parent Code']],
                defaults={'SegmentGrandParentLongName':
                          row[COLUMN_KEY['Segment Grand Parent Long Name']]},
            )
            obj_segment_parent, created = SegmentParent.objects.get_or_update(
                SegmentParentCode=row[COLUMN_KEY['Segment Parent Code']],
                defaults={'SegmentGrandParentCode': obj_segment_gp,
                          'SegmentParentLongName': row[COLUMN_KEY['Segment Parent Long Name']]},
            )
            obj_segment, created = Segment.objects.get_or_update(
                SegmentCode=row[COLUMN_KEY['Segment Code']],
                defaults={'SegmentParentCode': obj_segment_parent,
                          'SegmentLongName': row[COLUMN_KEY['Segment Long Name']]},
            )
            obj_er, created = EstimateRow.objects.get_or_update(
                EstimatesRowCode=row[COLUMN_KEY['Estimates Row Code']],
                defaults={'EstimatesRowLongName': row[COLUMN_KEY['Estimates Row Long Name']]},
            )
            obj_subsegment, created = SubSegment.objects.get_or_update(
                SubSegmentCode=row[COLUMN_KEY['Sub Segment Code']],
                defaults={'SegmentCode': obj_segment,
                          'SubSegmentLongName': row[COLUMN_KEY['Sub Segment Long Name']],
                          'ControlBudgetDetailCode': row[COLUMN_KEY['Control Budget Code']],
                          'EstimatesRowCode': obj_er,
                          'NetSubheadCode': row[COLUMN_KEY['Net Subhead Code']],
                          'PolicyRingfenceCode': row[COLUMN_KEY['Accounting Authority Code']],
                          'AccountingAuthorityCode': row[COLUMN_KEY['Policy Ringfence Code']],
                          'AccountingAuthorityDetailCode':
                              row[COLUMN_KEY['Accounting Authority Detail Code']]},
            )
