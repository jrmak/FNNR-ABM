# !/usr/bin/python

"""
This document imports household, individual, and land parcel data from the excel file.
It also converts the imported data into workable values.
"""

from openpyxl import *
import inspect
from excel_import import *

# Directory in which source file is located, exact name of source file + extension
currentpath2014 = str(inspect.getfile(inspect.currentframe()))[:-21] # 'removes excel_import_2014.py' at end
os.chdir(currentpath2014)
currentbook2014 = '2014_survey_validation_edited.xlsx'


# openpyxl commands
wbglobal2014 = load_workbook(currentbook2014)
sheet2014 = wbglobal2014.active

def assign_sheet_parameters_2014(hh_row, variable):
    """Given a household id and name of variable, returns cell range for given variable"""
    """Will create a new function when this list gets long enough"""
    parameters = []
    row = str(int(hh_row))
    # print(row) # For example, row 3 in the Excel file corresponds to Household ID #1
    # all lowercase!
    if variable.lower() == '2014_hh_id':
        parameters.append(str('B' + row))
        parameters.append(str('B' + row))
    elif variable.lower() == 'hh_id':
        parameters.append(str('A' + row))
        parameters.append(str('A' + row))
    elif variable.lower() == 'name':
        parameters.append(str('C' + row))
        parameters.append(str('K' + row))
    elif variable.lower() == 'age':
        parameters.append(str('U' + row))
        parameters.append(str('AC' + row))
    elif variable.lower() == 'gender':
        parameters.append(str('L' + row))
        parameters.append(str('T' + row))
    elif variable.lower() == 'education':
        parameters.append(str('AD' + row))
        parameters.append(str('AL' + row))
    elif variable.lower() == 'marriage':
        parameters.append(str('AM' + row))
        parameters.append(str('AU' + row))
    elif variable.lower() == 'workstatus':
        parameters.append(str('AV' + row))
        parameters.append(str('BD' + row))
    elif variable.lower() == 'migration_network':
        parameters.append(str('BG' + row))
        parameters.append(str('BG' + row))
    elif variable.lower() == 'non_gtgp_area':
        parameters.append(str('BW' + row))
        parameters.append(str('CA' + row))
    elif variable.lower() == 'gtgp_area':
        parameters.append(str('BR' + row))
        parameters.append(str('BV' + row))

    elif variable.lower() == 'non_gtgp_rice_mu':
        parameters.append(str('BN' + row))
        parameters.append(str('BN' + row))
    elif variable.lower() == 'gtgp_rice_mu':
        parameters.append(str('BP' + row))
        parameters.append(str('BP' + row))
    elif variable.lower() == 'non_gtgp_dry_mu':
        parameters.append(str('BO' + row))
        parameters.append(str('BO' + row))
    elif variable.lower() == 'gtgp_dry_mu':
        parameters.append(str('BQ' + row))
        parameters.append(str('BQ' + row))

    elif variable.lower() == 'non_gtgp_plant_type':
        parameters.append(str('IB' + row))
        parameters.append(str('IF' + row))
    elif variable.lower() == 'pre_gtgp_plant_type':
        parameters.append(str('CB' + row))
        parameters.append(str('CF' + row))
    elif variable.lower() == 'gtgp_travel_time':
        parameters.append(str('CG' + row))
        parameters.append(str('CK' + row))
    elif variable.lower() == 'non_gtgp_travel_time':
        parameters.append(str('IQ' + row))
        parameters.append(str('IU' + row))
    elif variable.lower() == 'pre_gtgp_output':
        parameters.append(str('CL' + row))
        parameters.append(str('CP' + row))
    elif variable.lower() == 'non_gtgp_output':
        parameters.append(str('CQ' + row))
        parameters.append(str('CU' + row))
    elif variable.lower() == 'pre_gtgp_land_type':
        parameters.append(str('CV' + row))
        parameters.append(str('CZ' + row))
    elif variable.lower() == 'non_gtgp_land_type':
        parameters.append(str('DA' + row))
        parameters.append(str('DE' + row))

    elif variable.lower() == ('initial_migrants'):
        parameters.append(str('BH' + row))
        parameters.append(str('BL' + row))

    elif variable.lower() == ('mig_remittances'):
        parameters.append(str('BM' + row))
        parameters.append(str('BM' + row))

    elif variable.lower() == ('income_local_off_farm'):
        parameters.append(str('BE' + row))
        parameters.append(str('BE' + row))

    # add more later; added variable strings must be lowercase
    else:
        print('Sorry,', variable, 'is not a valid variable category.')
        pass
    return parameters

def get_hh_row_2014(hh_id):
    """Returns an Excel household row when given the ID"""
    column_counter = 0
    for CellObj in sheet2014['A']:
        column_counter += 1
        if CellObj.value == hh_id:
            return column_counter


def initialize_labor_2014(hh_row):
    num_labor = 0
    # There are 94 total households, but ids range from 1-169.
    # for clarity: hh_row refers to the Excel spreadsheet row, 3-96 (representing 94 households).
    # hh_id refers to household ids as assigned in the Excel column, numbering from 1-169.
    agelist = return_values_2014(hh_row, 'age')  # find the ages of people in hh
    if agelist is not None:  # if there are people in the household,
        for age in agelist:  # for each person (can't use self.age because not a Household-level attribute),
                # ages are strings by default, must convert to float
            if 15 < float(age) < 59:  # if the person is 15-65 years old,
                num_labor += 1  # defines number of laborers as people aged 15 < x < 59
            #except:
            #    num_labor = 0
    else:
        print(hh_row, 'except2014')
    return num_labor

def initialize_migrants_2014(hh_row):
    if_migrant = return_values_2014(hh_row, 'initial_migrants')
    if if_migrant is not None and if_migrant[0] != -3:
        num_mig = 1
    else:
        num_mig = 0
    return num_mig

def assign_variable_per_hh_2014(x, y):
    """Adds value of a certain variable to that household's list"""
    var = []
    for Column in sheet2014[x:y]:
            for CellObj in Column:
                if x == y:
                    if CellObj.value not in ['-1', '-3', '-4', -1, -3, -4, None]:
                        # if the value is not null
                        var = str(CellObj.value)
                elif x != y:
                    # in this case, var is a list, not a str, because it has multiple items
                    if CellObj.value not in ['-1', '-3', '-4', -1, -3, -4, None]:
                        var.append(CellObj.value)
                        # var = str(CellObj.value)
    return var

def return_values_2014(hh_row, var):
    """Returns values given hh_id and variable (combines previous functions)"""
    # Example: return_values(1,'gender')
    hh_row_variable = assign_sheet_parameters_2014(hh_row, var)
    variable_per_hh = assign_variable_per_hh_2014(hh_row_variable[0], hh_row_variable[1])
    # print(variable_per_hh) # Example: ['1', '2', '1'] for genders in a household
    if variable_per_hh != []:
        return variable_per_hh

def initialize_labor_2014(hh_row):
    num_labor = 0
    agelist = return_values_2014(hh_row, 'age')  # find the ages of people in hh
    if agelist is not None:  # if there are people in the household,
        for age in agelist:  # for each person (can't use self.age because not a Household-level attribute),
                # ages are strings by default, must convert to float
            if 15 < float(age) < 59:  # if the person is 15-65 years old,
                num_labor += 1  # defines number of laborers as people aged 15 < x < 59
            #except:
            #    num_labor = 0
    else:
        print(hh_row, 'except')
    return num_labor

def initialize_migrants_2014(hh_row):
    if_migrant = return_values_2014(hh_row, 'initial_migrants')
    if if_migrant is not None and if_migrant[0] != -3:
        num_mig = 1
    else:
        num_mig = 0
    return num_mig