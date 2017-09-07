# !/usr/bin/python

import csv
import inspect
import os

currentpath = str(inspect.getfile(inspect.currentframe()))[:-31]  # 'removes excel_import.py' at end
os.chdir(currentpath)

try:
    fnnr_export = open('FNNR-ABM_export_household_2014.csv', 'a+')  # a+ will create the file if it doesn't exist already
    # a is also preferred to w here to append, rather than overwrite, values
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open

def initialize_household_2014():
    filewriter = csv.writer(fnnr_export)
    filewriter.writerow(['Step', 'Current Year', 'Household ID', 'Laborers in Household',
                        'Migrants from Household', 'Household Size', 'Household Income'])
    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def save_2014(step_counter, current_year, hh_id, num_labor, num_mig, hh_size, income):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export_household_2014.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    fnnr_export.writelines(str(step_counter))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(current_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(hh_id))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(num_labor))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(num_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(hh_size))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(income))
    fnnr_export.writelines('\n')

    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def erase_household_2014():
    try:
        fnnr_export = open('FNNR-ABM_export_household_2014.csv', 'w+')  # a+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
        pass
    fnnr_export.close()