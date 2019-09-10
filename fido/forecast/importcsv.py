import csv

from chartofaccountDIT.models import Analysis1, Analysis2, NaturalCode, ProgrammeCode, ProjectCode

from core.importcsv import ImportInfo, csvheadertodict, get_fk, get_fk_from_field

from costcentre.models import CostCentre

from .models import FinancialPeriod, FinancialYear, MonthlyFigure


# define the column position in the csv file.
# it reflects the position of columns in the Oracle report used to download the actuals
# MONTH_KEY = {
#     ADIReport.apr.field_name: 'Apr'.lower(),
#     ADIReport.may.field_name: 'May'.lower(),
#     ADIReport.jun.field_name: 'Jun'.lower(),
#     ADIReport.jul.field_name: 'Jul'.lower(),
#     ADIReport.aug.field_name: 'Aug'.lower(),
#     ADIReport.sep.field_name: 'Sep'.lower(),
#     ADIReport.oct.field_name: 'Oct'.lower(),
#     ADIReport.nov.field_name: 'Nov'.lower(),
#     ADIReport.dec.field_name: 'Dec'.lower(),
#     ADIReport.jan.field_name: 'Jan'.lower(),
#     ADIReport.feb.field_name: 'Feb'.lower(),
#     ADIReport.mar.field_name: 'Mar'.lower(),
#     ADIReport.adj1.field_name: 'Adj01'.lower()}
#

# 'Cost Centre'
# 'Natural Account'
# 'Programme'
# 'Analysis'
# 'Analysis2'
# 'Spare2'
# 'Period'
# 'Value'


# define the column position in the csv file.
# it reflects the position of columns in the Oracle report used to download the actuals
# MONTH_KEY = {
#     ADIReport.apr.field_name: 'Apr',
#     ADIReport.may.field_name: 'May',
#     ADIReport.jun.field_name: 'Jun',
#     ADIReport.jul.field_name: 'Jul',
#     ADIReport.aug.field_name: 'Aug',
#     ADIReport.sep.field_name: 'Sep',
#     ADIReport.oct.field_name: 'Oct',
#     ADIReport.nov.field_name: 'Nov',
#     ADIReport.dec.field_name: 'Dec',
#     ADIReport.jan.field_name: 'Jan',
#     ADIReport.feb.field_name: 'Feb',
#     ADIReport.mar.field_name: 'Mar',
#     ADIReport.adj1.field_name: 'Adj_1'}


def get_month_dict():
    """Link the column names in the ADI file with the foreign key used in the MonthlyFigure to identify the period"""
    q = FinancialPeriod.objects.filter(period_calendar_code__gt=0).values('period_short_name')
    mydict = {}
    for e in q:
        perobj, msg = get_fk_from_field(FinancialPeriod,
                                        'period_short_name',
                                        e['period_short_name'])
        mydict[e['period_short_name'].lower()] = perobj
    return mydict


def import_adi_file(csvfile):
    """Read the ADI file and unpivot it to enter the MonthlyFigure data
    Hard coded the year because it is a temporary solution....
    The information is used to create the OSCAR report to be uploaded to Treasury"""
    finyear = 2019
    reader = csv.reader(csvfile)
    col_key = csvheadertodict(next(reader))
    line = 1
    finobj, msg = get_fk(FinancialYear, finyear)
    month_dict = get_month_dict()
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1
        errmsg = ''
        ccobj, msg = get_fk(CostCentre, row[col_key['cost centre']].strip())
        errmsg += msg
        nacobj, msg = get_fk(NaturalCode, row[col_key['natural account']].strip())
        errmsg += msg
        prog = row[col_key['programme']].strip()
        progobj, msg = get_fk(ProgrammeCode, prog)
        errmsg += msg
        an1obj, msg = get_fk(Analysis1, int(row[col_key['analysis']]))
        an2obj, msg = get_fk(Analysis2, int(row[col_key['analysis2']]))
        projobj, msg = get_fk(ProjectCode, row[col_key['spare2']].strip())
        # Now read the twelve month values into a dict
        if errmsg == '':
            for month, perobj in month_dict.items():
                period_amount = int(row[col_key[month.lower()]])
                adiobj, created = MonthlyFigure.objects.get_or_create(financial_year=finobj,
                                                                      programme=progobj,
                                                                      cost_centre=ccobj,
                                                                      natural_account_code=nacobj,
                                                                      analysis1_code=an1obj,
                                                                      analysis2_code=an2obj,
                                                                      project_code=projobj,
                                                                      financial_period=perobj)
                if created:
                    adiobj.amount = period_amount
                else:
                    adiobj.amount += period_amount
                adiobj.save()
        else:
            print(line, errmsg)

        if (line % 100) == 0:
            print(line)


h_list = ['cost centre',
          'natural account', 'programme', 'analysis', 'analysis2', 'spare2',
          'Apr',
          'May',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Oct',
          'Nov',
          'Dec',
          'Jan',
          'Feb',
          'Mar'
          ]

import_adi_file_class = ImportInfo({}, 'DIT Information',
                                   h_list,
                                   import_adi_file)


def import_unpivot_actual(csvfile, finyear):
    reader = csv.reader(csvfile)
    col_key = csvheadertodict(next(reader))
    print(col_key)
    line = 2
    finobj, msg = get_fk(FinancialYear, finyear)
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1
        errmsg = ''
        ccobj, msg = get_fk(CostCentre, row[col_key['cost centre']].strip())
        errmsg += msg
        nacobj, msg = get_fk(NaturalCode, row[col_key['natural account']].strip())
        errmsg += msg
        prog = row[col_key['programme']].strip()
        if prog == 0:
            prog = 310801
        progobj, msg = get_fk(ProgrammeCode, prog)
        errmsg += msg
        perobj, msg = get_fk_from_field(FinancialPeriod,
                                        'period_short_name',
                                        row[col_key['period']].strip()
                                        )
        errmsg += msg

        an1obj, msg = get_fk(Analysis1, int(row[col_key['analysis']]))
        an2obj, msg = get_fk(Analysis2, int(row[col_key['analysis2']]))
        projobj, msg = get_fk(ProjectCode, row[col_key['spare2']].strip())
        period_amount = int(row[col_key['amount']])
        if errmsg == '':
            adiobj, created = MonthlyFigure.objects.get_or_create(financial_year=finobj,
                                                                  programme=progobj,
                                                                  cost_centre=ccobj,
                                                                  natural_account_code=nacobj,
                                                                  analysis1_code=an1obj,
                                                                  analysis2_code=an2obj,
                                                                  project_code=projobj,
                                                                  financial_period=perobj)
            adiobj.amount = period_amount
            adiobj.save()
            if not line % 1000:
                print(line)
        else:
            print('Error at line ', line, errmsg)
