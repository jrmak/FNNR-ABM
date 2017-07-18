# !/usr/bin/python

import csv
import inspect
import os
from model import *

"""
Exports household-level aggregate data into Excel.
"""

"""Clear FNNR-ABM_export_individual.csv each time you run the model. Will figure out how to do this automatically later."""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-23]  # 'removes excel_import.py' at end
os.chdir(currentpath)

def initialize_summary():
    try:
        fnnr_export = open('FNNR-ABM_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    filewriter = csv.writer(fnnr_export)
    filewriter.writerow(['Years Elapsed', 'Average # of Migrants', 'Total # of Marriages', 'Total # of Births', 'Population'])

    fnnr_export.flush()  # flush memory
    fnnr_export.close()

def save_summary(steps, show_num_mig, show_marriages, show_births, population):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export_summary.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open

    fnnr_export.writelines(str(steps))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_num_mig))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_marriages))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(show_births))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(population))
    fnnr_export.writelines(',')
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()


def erase_summary():
    try:
        fnnr_export = open('FNNR-ABM_export_summary.csv', 'w+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
        fnnr_export.truncate()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    fnnr_export.close()