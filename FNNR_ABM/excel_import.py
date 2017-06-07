# !/usr/bin/python

"""
This document imports household, individual, and land parcel data from the excel file.
It also converts the imported data into workable values.
"""

from openpyxl import *

# Directory in which source file is located, exact name of source file + extension
os.chdir(r'C:\Users\jmak4\PycharmProjects\FNNR_ABM\FNNR_ABM')  #will need to replace
currentbook = 'FNNR_2016_Survey_psuedo_0602.xlsx'

# openpyxl commands
wbglobal = load_workbook(currentbook)
sheet = wbglobal.active

# a list of 96 hh_ids; hardcoded since number from excel file not likely to change
hh_id_list = list(range(1, 97))


def assign_sheet_parameters(hh_id, variable):
    """Given a household id and name of variable, returns cell range for given variable"""
    parameters = []
    row = str(hh_id + 2)
    # all lowercase!
    if variable.lower() == 'gtgp_area':
        parameters.append(str('DM' + row))
        parameters.append(str('DQ' + row))
    elif variable.lower() == 'age':
        parameters.append(str('AG' + row))
        parameters.append(str('AO' + row))
    elif variable.lower() == 'education':
        parameters.append(str('AY' + row))
        parameters.append(str('BG' + row))
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
    elif variable.lower() == 'num_mig':
        parameters.append(str('ZV' + row))
        parameters.append(str('ZZ' + row))
    # add more later; added variable strings must be lowercase
    else:
        print('Sorry,', variable, 'is not a valid variable category.')
        pass
    return parameters

def assign_variable_per_hh(x, y):
    """Adds value of a certain variable to that household's list"""
    var = []
    for Column in sheet[x:y]:
            for CellObj in Column:
                if x == y:
                    if CellObj.value not in [-1, -3, '-1', '-3']:
                        # if the value is not null
                        var = str(CellObj.value)
                elif x != y:
                    # in this case, var is a list, not a str, because it has multiple items
                    if CellObj.value not in [-1, -3, '-1', '-3']:
                        var.append(CellObj.value)
                        # var = str(CellObj.value)
    return var

def return_values(hh_id, var):
    """Returns values given hh_id and variable (combines previous functions)"""
    # Example: return_values(1,'gender')
    hh_id_variable = assign_sheet_parameters(hh_id, var)
    # print(hh_id_variable) # Example: ['A3', 'AF3'] if argument is (1, 'gender')
    variable_per_hh = assign_variable_per_hh(hh_id_variable[0], hh_id_variable[1])
    # print(variable_per_hh) # Example: ['1', '2', '1'] for genders in a household
    return variable_per_hh

def convert_lat_long(coord):
    """Converts coordinates from format 27,59,30.747 to 27.99184177"""
    coordlist = coord.strip("[]").split(",")
    for coordx in coordlist:
        coordx.replace(coordx, coordx.strip("'").strip(" "))
        # print(coordlist)
    if coordlist[0] is not None and coordlist[0] != '':
        degree = int(coordlist[0].strip("'"))
        minutes = int(coordlist[1])
        seconds = float(coordlist[2].strip("'"))
        converted = degree + (minutes / 60) + (seconds / 3600)
        return converted

def convert_fraction_lat(coord):
    """Converts coordinates into fractions to fit into continuous space"""
    # print(coord, ' latitude')
    # degrees North; determines x-axis bounds of map area on simulation
    lowerbound = 27.95
    upperbound = 28
    try:
        result = (coord - lowerbound) / (upperbound - lowerbound)
        # print(result, ' lat result')
        if result < 1:  # some errant latitudes at 27.65
            return result
    except:
        pass  # skips over instances where coordinate is empty

def convert_fraction_long(coord):
    """Converts coordinates into fractions to fit into continuous space"""
    # print(coord,' longitude')
    # degrees East; determines y-axis bounds of map area on simulation
    lowerbound = 108.65
    upperbound = 108.83
    try:
        result = (coord - lowerbound) / (upperbound - lowerbound)
        # print(result, 'long result')
        return result
    except:
        pass  # skips over instances where coordinate is empty

def convert_num_mig(mig_value_list):
    """Converts excel values to actual numbers"""
    num_mig_counter = 0
    for value in mig_value_list:
        if value is not 'None':
            num_mig_counter += 1
    return num_mig_counter
