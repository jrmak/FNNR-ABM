# !/usr/bin/python

"""
This document imports household, individual, and land parcel data from the excel file.
It also converts the imported data into workable values.
"""

from openpyxl import *
import inspect

# Directory in which source file is located, exact name of source file + extension
currentpath = str(inspect.getfile(inspect.currentframe()))[:-16] # 'removes excel_import.py' at end
os.chdir(currentpath)
currentbook = 'FNNR_2016_Survey_psuedo_0726.xlsx'


# openpyxl commands
wbglobal = load_workbook(currentbook)
sheet = wbglobal.active

# a list of 94 hh_ids; hardcoded since number from excel file not likely to change
agents = list(range(1, 95))  # range(1, 95) goes 1-94

def assign_sheet_parameters(hh_row, variable):
    """Given a household id and name of variable, returns cell range for given variable"""
    """Will create a new function when this list gets long enough"""
    parameters = []
    row = str(int(hh_row) + 2)
    # print(row) # For example, row 3 in the Excel file corresponds to Household ID #1
    # all lowercase!
    if variable.lower() == 'gtgp_area':
        parameters.append(str('DM' + row))
        parameters.append(str('DQ' + row))
    elif variable.lower() == 'hh_id':
        parameters.append(str('A' + row))
        parameters.append(str('A' + row))
    elif variable.lower() == 'name':
        parameters.append(str('F' + row))
        parameters.append(str('N' + row))
    elif variable.lower() == 'age':
        parameters.append(str('AG' + row))
        parameters.append(str('AO' + row))
    elif variable.lower() == 'gender':
        parameters.append(str('X' + row))
        parameters.append(str('AF' + row))
    elif variable.lower() == 'education':
        parameters.append(str('AY' + row))
        parameters.append(str('BG' + row))
    elif variable.lower() == 'marriage':
        parameters.append(str('BH' + row))
        parameters.append(str('BP' + row))
    elif variable.lower() == 'workstatus':
        parameters.append(str('BQ' + row))
        parameters.append(str('BY' + row))
    elif variable.lower() == 'house_longitude':
        parameters.append(str('CA' + row))
        parameters.append(str('CA' + row))
    elif variable.lower() == 'house_latitude':
        parameters.append(str('CB' + row))
        parameters.append(str('CB' + row))
    elif variable.lower() == 'gtgp_longitude':
        parameters.append(str('DW' + row))
        parameters.append(str('EA' + row))
    elif variable.lower() == 'gtgp_latitude':
        parameters.append(str('EB' + row))
        parameters.append(str('EF' + row))
    elif variable.lower() == 'non_gtgp_longitude':
        parameters.append(str('JK' + row))
        parameters.append(str('JO' + row))
    elif variable.lower() == 'non_gtgp_latitude':
        parameters.append(str('JP' + row))
        parameters.append(str('JT' + row))
    elif variable.lower() == 'migration_network':
        parameters.append(str('AIP' + row))
        parameters.append(str('AIP' + row))

    elif variable.lower() == 'non_gtgp_rice_mu':
        parameters.append(str('CU' + row))
        parameters.append(str('CU' + row))
    elif variable.lower() == 'gtgp_rice_mu':
        parameters.append(str('CW' + row))
        parameters.append(str('CW' + row))
    elif variable.lower() == 'non_gtgp_dry_mu':
        parameters.append(str('CX' + row))
        parameters.append(str('CX' + row))
    elif variable.lower() == 'gtgp_dry_mu':
        parameters.append(str('DB' + row))
        parameters.append(str('DB' + row))
    elif variable.lower() == 'non_gtgp_plant_type':
        parameters.append(str('IB' + row))
        parameters.append(str('IF' + row))
    elif variable.lower() == 'pre_gtgp_plant_type':
        parameters.append(str('DC' + row))
        parameters.append(str('DG' + row))
    elif variable.lower() == 'gtgp_travel_time':
        parameters.append(str('EQ' + row))
        parameters.append(str('EU' + row))
    elif variable.lower() == 'non_gtgp_travel_time':
        parameters.append(str('IQ' + row))
        parameters.append(str('IU' + row))
    elif variable.lower() == 'pre_gtgp_output':
        parameters.append(str('GY' + row))
        parameters.append(str('HC' + row))
    elif variable.lower() == 'non_gtgp_output':
        parameters.append(str('KE' + row))
        parameters.append(str('KI' + row))
    elif variable.lower() == 'pre_gtgp_land_type':
        parameters.append(str('DC' + row))
        parameters.append(str('DG' + row))
    elif variable.lower() == 'non_gtgp_land_type':
        parameters.append(str('IB' + row))
        parameters.append(str('IF' + row))

    elif variable.lower() == ('initial_migrants'):
        parameters.append(str('AIQ' + row))
        parameters.append(str('AIU' + row))

    elif variable.lower() == ('mig_remittances'):
        parameters.append(str('AIV' + row))
        parameters.append(str('AIV' + row))

    elif variable.lower() == ('income_local_off_farm'):
        parameters.append(str('AIW' + row))
        parameters.append(str('AIW' + row))

    elif variable.lower() == 'remittance_prev':
        parameters.append(str('AHT' + row))
        parameters.append(str('AHT' + row))

    # add more later; added variable strings must be lowercase
    else:
        print('Sorry,', variable, 'is not a valid variable category.')
        pass
    return parameters

def get_hh_row(hh_id):
    """Returns an Excel household row when given the ID"""
    column_counter = 0
    for CellObj in sheet['A']:
        column_counter += 1
        if CellObj.value == hh_id:
            return column_counter


def initialize_labor(hh_row):
    """Returns an initial # of laborers for a given household"""
    num_labor = 0
    # There are 94 total households, but ids range from 1-169.
    # for clarity: hh_row refers to the Excel spreadsheet row, 3-96 (representing 94 households).
    # hh_id refers to household ids as assigned in the Excel column, numbering from 1-169.
    agelist = return_values(hh_row, 'age')  # find the ages of people in hh
    if agelist is not None:  # if there are people in the household,
        for age in agelist:  # for each person (can't use self.age because not a Household-level attribute),
                # ages are strings by default, must convert to float
            if 15 < float(age) < 59:  # if the person is 15-65 years old,
                num_labor += 1  # defines number of laborers as people aged 15 < x < 59
            #except:
            #    num_labor = 0
    return num_labor

def initialize_migrants(hh_row):
    if_migrant = return_values(hh_row, 'initial_migrants')
    if if_migrant is not None and if_migrant[0] != -3:
        num_mig = 1
    else:
        num_mig = 0
    return num_mig

def assign_variable_per_hh(x, y):
    """Adds value of a certain variable to that household's list"""
    var = []
    for Column in sheet[x:y]:
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


def return_values(hh_row, var):
    """Returns values given hh_id and variable (combines previous functions)"""
    # Example: return_values(1,'gender')
    hh_row_variable = assign_sheet_parameters(hh_row, var)
    variable_per_hh = assign_variable_per_hh(hh_row_variable[0], hh_row_variable[1])
    # print(variable_per_hh) # Example: ['1', '2', '1'] for genders in a household
    if variable_per_hh != []:
        return variable_per_hh


def convert_decimal(coord):
    """Converts coordinates from format 27,59,30.747 to 27.99184177"""
    convertedlist = []
    coordlist = coord.strip("[]").split(",")
    for coordx in coordlist:
        coordx.replace(coordx, coordx.strip("'").strip(" "))
    if coordlist[0] != 'None' and coordlist[0] != '' and coordlist[0] != '-4':
        indexlist = [0, 3, 6, 9, 12, 15]
        for i in indexlist:
            try:
                degree = int(coordlist[i].strip("'").strip(" ").replace("'", ''))
                minutes = int(coordlist[i + 1])
                seconds = float(coordlist[i + 2].strip("'"))
                converted = degree + (minutes / 60) + (seconds / 3600)
                convertedlist.append(converted)
            except:
                break
        return (convertedlist)


def convert_fraction_lat(coordlist):
    """Converts coordinates into fractions to fit into continuous space"""
    # print(coord, ' latitude')
    # degrees North; determines x-axis bounds of map area on simulation
    lowerbound = 27.95
    upperbound = 28
    convertedlist = []
    for coord in coordlist:
        try:
            result = (coord - lowerbound) / (upperbound - lowerbound)
            # print(result, ' lat result')
            if result < 1:  # some errant latitudes at 27.65
                convertedlist.append(result)
        except:
            pass  # skips over instances where coordinate is empty
        # print(convertedlist)
    return convertedlist


def convert_fraction_long(coordlist):
    """Converts coordinates into fractions to fit into continuous space"""
    # print(coord,' longitude')
    # degrees East; determines y-axis bounds of map area on simulation
    lowerbound = 108.65
    upperbound = 108.83
    convertedlist = []
    for coord in coordlist:
        try:
            result = (coord - lowerbound) / (upperbound - lowerbound)
            convertedlist.append(result)
        except:
            pass  # skips over instances where coordinate is empty
    return convertedlist