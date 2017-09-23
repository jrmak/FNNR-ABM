# !/usr/bin/python

import csv
import inspect
import os
from model import *

"""
Exports household-level aggregate data into Excel.
"""
currentpath = str(inspect.getfile(inspect.currentframe()))[:-23]  # 'removes excel_import_summary.py' at end
os.chdir(currentpath)


def save_summary(steps, show_cumulative_mig, show_num_mig, show_num_mig_per_year,
                 show_cumulative_re_mig, show_re_mig, show_re_mig_per_year, show_marriages,
                 show_births, show_deaths, show_num_labor, show_hh_size, show_income,
                 population, show_gtgp_per_hh, show_non_gtgp_per_hh):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export_summary_2016.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    if steps == 0:
        filewriter = csv.writer(fnnr_export)
        filewriter.writerow(
            ['Years Elapsed', 'Cumulative Out-Migrants', 'Instant Out-Migrants', 'Average Out-Migrants',
             'Total Re-Migrants', 'Instant Re-Migrants', 'Average Re-Migrants',
             'Total Marriages', 'Total Births', 'Total Deaths', 'Average Laborers', 'Average Household Size',
             'Average Income',
             'Population', 'GTGP Parcels Per Household', 'Non-GTGP Parcels Per Household'])
    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_cumulative_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_num_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_num_mig_per_year))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_cumulative_re_mig))
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
    fnnr_export.writelines(str(show_num_labor))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_hh_size))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_income))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(population))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_gtgp_per_hh))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_non_gtgp_per_hh))
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()


def erase_summary():
    try:
        fnnr_export = open('FNNR-ABM_export_summary_2016.csv', 'w+')  # a+ will create the file if it doesn't exist already
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()