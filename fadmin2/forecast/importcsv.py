from django.core.exceptions import ObjectDoesNotExist
import csv

from .models import ADIReport, SubSegmentUKTIMapping
from core.myutils import addposition,csvheadertodict


from costcentre.models import CostCentre, Programme
from chartofaccountDIT.models import NaturalCode, Analysis1, Analysis2

# define the column position in the csv file.
# it reflects the position of columns in the Oracle report used to download the actuals


MONTH_KEY= {
            ADIReport.apr.field_name : 'Apr',
            ADIReport.may.field_name : 'May',
            ADIReport.jun.field_name : 'Jun',
            ADIReport.jul.field_name : 'Jul',
            ADIReport.aug.field_name : 'Aug',
            ADIReport.sep.field_name : 'Sep',
            ADIReport.oct.field_name : 'Oct',
            ADIReport.nov.field_name : 'Nov',
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

    reader = csv.reader(csvfile)
    col_key = csvheadertodict(next(reader))
    line = 2
    actualtoimport={}
    if what == 'ALL':
        actualtoimport = MONTH_KEY
    else:
        actualtoimport[findmonth(what)] = what
    # translate the key to the column number
    actualtoimport = addposition(actualtoimport, col_key)
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1

        try:
            ccobj = CostCentre.objects.get(cost_centre_code=row[col_key['Cost Centre']])
            an1obj = Analysis1.objects.get(analysis1_code=int(row[col_key['Analysis 1']]))
            an2obj = Analysis2.objects.get(analysis2_code=int(row[col_key['Analysis 2']]))
            nacobj = NaturalCode.objects.get(natural_account_code=row[col_key['Account']])
            prog = row[col_key['Programme']]
            if prog == 0:
                prog = 310801
            progobj = Programme.objects.get(programme_code=prog)
            defaultList = {}
            print(line)
            for k, v in actualtoimport.items():
                defaultList[k] = row[v] or 0
            adiobj, created = ADIReport.objects.get_or_create(financial_year=financialyear,
                                                              programme=progobj,
                                                              cost_centre=ccobj,
                                                              natural_account_code=nacobj,
                                                              analysis1_code=an1obj,
                                                              analysis2_code=an2obj,
                                                              defaults=defaultList)

        except ObjectDoesNotExist:
            print('Cost centre ', row[col_key['Cost Centre']], ' does not exist')
# todo handle error from missing codes, create the list from ALL based on file content

