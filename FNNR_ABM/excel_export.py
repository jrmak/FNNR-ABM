from openpyxl import *


def save(entries):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export.csv', 'w+')  # w+ will create the file if it doesn't exist already
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    #for agent in agentlists:
    try:
        fnnr_export.writelines(self.hh_id)
        fnnr_export.writelines(',')
        fnnr_export.writelines(self.individual_id)
        fnnr_export.writelines(',')
        fnnr_export.writelines(self.)
        fnnr_export.writelines(',')
        fnnr_export.writelines()
        fnnr_export.writelines(',')
        fnnr_export.writelines()
        fnnr_export.writelines(',')
        fnnr_export.writelines()
        fnnr_export.writelines(',')
        fnnr_export.writelines()
        fnnr_export.writelines(',')
        fnnr_export.writelines()
        fnnr_export.writelines('\n')
    except KeyError:
        continue   # sometimes places bring up error when items don't exist
    fnnr_export.flush()  # flush memory
    fnnr_export.close()
    print('Saved to .csv')