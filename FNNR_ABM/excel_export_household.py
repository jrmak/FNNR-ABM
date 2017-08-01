# !/usr/bin/python

import csv
import inspect
import os

"""Clear FNNR-ABM_export_individual.csv each time you run the model. Figuring out how to do this automatically later."""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-26]  # 'removes excel_import.py' at end
os.chdir(currentpath)

try:
    fnnr_export = open('FNNR-ABM_export_household.csv', 'a+')  # a+ will create the file if it doesn't exist already
    # a is also preferred to w here to append, rather than overwrite, values
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open

# fnnr_export.flush()  # flush memory
# fnnr_export.close()

def save(step_counter, current_year, hh_id, num_labor, num_mig, income, hh_size):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export_household.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if step_counter == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(['Step', 'Current Year', 'Household ID', 'Laborers in Household',
                         'Migrants from Household', 'Household Income', 'Household Size'])


    fnnr_export.writelines(str(step_counter))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(current_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(hh_id))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(num_labor))
    fnnr_export.writelines('\n')
    fnnr_export.writelines(str(num_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(income))
    fnnr_export.writelines('\n')
    fnnr_export.writelines(str(hh_size))
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()


def erase_household():
    try:
        fnnr_export = open('FNNR-ABM_export_household.csv', 'w+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()