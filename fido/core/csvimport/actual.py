import csv

from chartofaccountDIT.models import ADIReport, Analysis1, Analysis2, NaturalCode, ProgrammeCode

from core.myutils import addposition

from costcentre.models import CostCentre

from django.core.exceptions import ObjectDoesNotExist

# define the column position in the csv file.
# it reflects the position of columns in the Oracle report used to download the actuals

COLUMN_KEY = {
    'Entity': 0,
    'Cost Centre': 1,
    'Account': 2,
    'Programme': 3,
    'Analysis 1': 4,
    'Analysis 2': 5,
    'Apr': 6,
    'May': 7,
    'Jun': 8,
    'Jul': 9,
    'Aug': 10,
    'Sep': 11,
    'Oct': 12,
    'Nov': 13,
    'Dec': 14,
    'Jan': 15,
    'Feb': 16,
    'Mar': 17,
    'Adj_1': 18,
    'Adj_2': 19,
    'Adj_3': 20}

MONTH_KEY = {
    ADIReport.April.field_name: 'Apr',
    ADIReport.May.field_name: 'May',
    ADIReport.June.field_name: 'Jun',
    ADIReport.July.field_name: 'Jul',
    ADIReport.August.field_name: 'Aug',
    ADIReport.September.field_name: 'Sep',
    ADIReport.October.field_name: 'Oct',
    ADIReport.November.field_name: 'Nov',
    ADIReport.December.field_name: 'Dec',
    ADIReport.January.field_name: 'Jan',
    ADIReport.February.field_name: 'Feb',
    ADIReport.March.field_name: 'Mar',
    ADIReport.Adjustment1.field_name: 'Adj_1'}


# ADIReport.Adjustment1.field_name: 'Adj_1',
# ADIReport.Adjustment2.field_name: 'Adj_2',
# ADIReport.Adjustment3.field_name: 'Adj_3'}


# return the name of thefield associated with the required month
def findmonth(monthtofind):
    for k, v in MONTH_KEY.items():
        if v == monthtofind:
            return k


def import_actual(csvfile, financialyear, what):
    has_header = csv.Sniffer().has_header(csvfile.read())
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    line = 1
    if has_header:
        next(reader)  # Skip header row.
    actualtoimport = {}
    if what == 'ALL':
        actualtoimport = MONTH_KEY
    else:
        actualtoimport[findmonth(what)] = what
    # translate the key to the column number
    actualtoimport = addposition(actualtoimport, COLUMN_KEY)
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1

        try:
            ccobj = CostCentre.objects.get(CCCode=row[COLUMN_KEY['Cost Centre']])
            an1obj = Analysis1.objects.get(Analysis1Code=int(row[COLUMN_KEY['Analysis 1']]))
            an2obj = Analysis2.objects.get(Analysis2Code=int(row[COLUMN_KEY['Analysis 2']]))
            nacobj = NaturalCode.objects.get(NaturalAccountCode=row[COLUMN_KEY['Account']])
            prog = row[COLUMN_KEY['Programme']]
            if prog == 0:
                prog = 310801
            progobj = ProgrammeCode.objects.get(ProgrammeCode=prog)
            defaultList = {}
            print(line)
            for k, v in actualtoimport.items():
                defaultList[k] = row[v] or 0
            adiobj, created = ADIReport.objects.get_or_create(FinancialYear=financialyear,
                                                              Programme=progobj,
                                                              CCCode=ccobj,
                                                              NaturalAccountCode=nacobj,
                                                              Analysis1Code=an1obj,
                                                              Analysis2Code=an2obj,
                                                              defaults=defaultList)

        except ObjectDoesNotExist:
            print('Cost centre ', row[COLUMN_KEY['Cost Centre']], ' does not exist')
# todo handle error from missing codes, create the list from ALL based on file content
