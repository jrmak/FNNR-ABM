from openpyxl import *

os.chdir(r'C:\Users\jmak4\Desktop\FNNR-ABM\2016-Survey-Data')
currentbook = 'FNNR_2016_Survey_data_request_4-14.xlsx'

wbglobal = load_workbook(currentbook)
sheet = wbglobal.active

#a list of 96 hh_ids; hardcoded since number not likely to change
hh_id_list = list(range(1,97))

def assign_sheet_parameters(hh_id, variable):
    """Given a household id and name of variable, returns cell range for given variable"""
    parameters = []
    row = str(hh_id + 2)
    if variable.lower() == 'gender':
        parameters.append(str('X'+ row))
        parameters.append(str('AF' + row))
    elif variable.lower() == 'age':
        parameters.append(str('AG'+ row))
        parameters.append(str('AO' + row))
    elif variable.lower() == 'education':
        parameters.append(str('AY'+ row))
        parameters.append(str('BG' + row))
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
    #add more later
    else:
        print('Sorry, that is not a valid variable category.')
        pass
    return parameters

def assign_variable_per_hh(x, y):
    """Adds value of a certain variable to that household's list"""
    var = []
    for Column in sheet[x:y]:
            for CellObj in Column:
                if x == y:
                    if CellObj.value != -3 and CellObj.value != -1:
                        var = str(CellObj.value)
                elif x!= y:
                    if CellObj.value != -3 and CellObj.value != -1:
                        #var.append(CellObj.value) #last parcel only
                        var = str(CellObj.value)
                        pass
                else:
                    pass
    return var

def return_values(x,y):
    """Returns values given hh_id and variable (combines previous functions)"""
    hh_id_variable = assign_sheet_parameters(x,y)
    #print(hh_id_variable) #Example: ['A3', 'AF3'] if argument is (1, 'gender')
    variable_per_hh = assign_variable_per_hh(hh_id_variable[0], hh_id_variable[1])
    #print(variable_per_hh) #Example: returns genders of individuals in the first hh as a list
    return variable_per_hh

def convert_lat_long(coord):
    """Converts coordinates from format 27,59,30.747 to 27.99184177"""
    coordlist = coord.strip("[]").split(",")
    try:
        degree = int(coordlist[0])
        minutes = int(coordlist[1])
        seconds = float(coordlist[2])
        converted = degree + (minutes / 60) + (seconds / 3600)
        return converted
    except:
        pass

def convert_fraction_lat(coord):
    """Converts coordinates into fractions to fit into continuous space"""
    #print(coord, ' latitude')
    lowerbound = 27.95
    upperbound = 28
    try:
        result = (coord - lowerbound) / (upperbound - lowerbound)
        #print(result, ' lat result')
        if result < 1: #some errant latitudes at 27.65
            return result
    except:
        pass

def convert_fraction_long(coord):
    """Converts coordinates into fractions to fit into continuous space"""
    #print(coord,' longitude')
    lowerbound = 108.65
    upperbound = 108.83
    try:
        result = (coord - lowerbound) / (upperbound - lowerbound)
        #print(result, 'long result')
        return result
    except:
        pass