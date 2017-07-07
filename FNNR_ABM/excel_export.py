from openpyxl import *


def save(step_counter, individual_id, marriage):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export.csv', 'w+')  # w+ will create the file if it doesn't exist already
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    #for agent in agentlists:
    try:
        print(step_counter)
        fnnr_export.writelines(['1', '2', '3'])
        fnnr_export.writelines(',')
        print(individual_id)
        #fnnr_export.write(str(individual_id))
        #fnnr_export.write(',')
        print(marriage)
        #fnnr_export.write(str(marriage))
        fnnr_export.writelines('\n')
    except KeyError:
        pass   # sometimes places bring up error when items don't exist
    fnnr_export.flush()  # flush memory
    fnnr_export.close()
    print('Saved to .csv')
