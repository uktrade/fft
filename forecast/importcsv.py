import csv

from chartofaccountDIT.models import Analysis1, Analysis2, NaturalCode, ProgrammeCode

from core.importcsv import addposition, csvheadertodict, get_fk

from costcentre.models import CostCentre

from .models import ADIReport


# define the column position in the csv file.
# it reflects the position of columns in the Oracle report used to download the actuals
MONTH_KEY = {
    ADIReport.apr.field_name: 'Apr',
    ADIReport.may.field_name: 'May',
    ADIReport.jun.field_name: 'Jun',
    ADIReport.jul.field_name: 'Jul',
    ADIReport.aug.field_name: 'Aug',
    ADIReport.sep.field_name: 'Sep',
    ADIReport.oct.field_name: 'Oct',
    ADIReport.nov.field_name: 'Nov',
    ADIReport.dec.field_name: 'Dec',
    ADIReport.jan.field_name: 'Jan',
    ADIReport.feb.field_name: 'Feb',
    ADIReport.mar.field_name: 'Mar',
    ADIReport.adj1.field_name: 'Adj_1'}


# ADIReport.Adjustment1.field_name: 'Adj_1',
# ADIReport.Adjustment2.field_name: 'Adj_2',
# ADIReport.Adjustment3.field_name: 'Adj_3'}


# return the name of thefield associated with the required month
def findmonth(monthtofind):
    for k, v in MONTH_KEY.items():
        if v == monthtofind:
            return k


def import_actual(csvfile, financialyear, what):
    """ it imports the actuals from a report created in Oracle"""
    reader = csv.reader(csvfile)
    col_key = csvheadertodict(next(reader))
    line = 2
    actualtoimport = {}
    if what == 'ALL':
        actualtoimport = MONTH_KEY
    else:
        actualtoimport[findmonth(what)] = what
    # translate the key to the column number
    actualtoimport = addposition(actualtoimport, col_key)
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1
        errmsg = ''
        ccobj, msg = get_fk(CostCentre, row[col_key['Cost Centre']].strip())
        errmsg += msg
        an1obj, msg = get_fk(Analysis1, int(row[col_key['Analysis 1']]))
        errmsg += msg
        an2obj, msg = get_fk(Analysis2, int(row[col_key['Analysis 2']]))
        errmsg += msg
        nacobj, msg = get_fk(NaturalCode, row[col_key['Account']].strip())
        errmsg += msg
        prog = row[col_key['Programme']].strip()
        if prog == 0:
            prog = 310801
        progobj, msg = get_fk(ProgrammeCode, prog)
        errmsg += msg
        if errmsg == '':
            defaultList = {}
            for k, v in actualtoimport.items():
                defaultList[k] = row[v] or 0
            adiobj, created = ADIReport.objects.get_or_create(financial_year=financialyear,
                                                              programme=progobj,
                                                              cost_centre=ccobj,
                                                              natural_account_code=nacobj,
                                                              analysis1_code=an1obj,
                                                              analysis2_code=an2obj,
                                                              defaults=defaultList)
        else:
            print(line, errmsg)
# todo handle error from missing codes, create the list from ALL based on file content
