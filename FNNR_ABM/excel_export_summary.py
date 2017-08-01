# !/usr/bin/python

import csv
import inspect
import os
from model import *

"""
Exports household-level aggregate data into Excel.
"""

"""Clear FNNR-ABM_export_individual.csv each time you run the model. Will figure out how to do this automatically later."""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-23]  # 'removes excel_import_summary.py' at end
os.chdir(currentpath)

# try:
#     fnnr_export = open('FNNR-ABM_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
#     # a is also preferred to w here to append, rather than overwrite, values
# except IOError:
#     print('Please close Excel and retry.')  # will not work if the .csv is already open
#
# filewriter = csv.writer(fnnr_export)
# filewriter.writerow(['Years Elapsed', 'Average Migrants Per Household', 'Total Marriages', 'Total Births', 'Population'])
#
# fnnr_export.flush()  # flush memory
# fnnr_export.close()

def save_summary(steps, show_num_mig, show_num_mig_per_year, show_re_mig, show_re_mig_per_year, show_marriages,
                 show_births, show_deaths, show_marriages_per_year, show_births_per_year, show_deaths_per_year,
                 population, show_gtgp_per_hh):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Years Elapsed', 'Total Out-Migrants', 'Average Out-Migrants', 'Total Re-Migrants', 'Average Re-Migrants',
             'Total Marriages', 'Total Births', 'Total Deaths', 'New Marriages', 'New Births', 'New Deaths',
             'Population', 'GTGP Parcels Per Household'])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_num_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_num_mig_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_re_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_re_mig_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_marriages))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_births))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_deaths))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_marriages_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_births_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_deaths_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(population))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_gtgp_per_hh))
    fnnr_export.writelines(',')
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()


def erase_summary():
    try:
        fnnr_export = open('FNNR-ABM_export_summary.csv', 'w+')  # a+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()