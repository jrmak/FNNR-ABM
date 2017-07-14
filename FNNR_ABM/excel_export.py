import csv
import inspect
import os

# !/usr/bin/python

"""Clear FNNR-ABM_export.csv each time you run the model. Figuring out how to do this automatically later."""

currentpath = str(inspect.getfile(inspect.currentframe()))[:-16]  # 'removes excel_import.py' at end
os.chdir(currentpath)
print("Find FNNR-ABM_export.csv in: " + str(currentpath))

try:
    fnnr_export = open('FNNR-ABM_export.csv', 'a+')  # a+ will create the file if it doesn't exist already
    # a is also preferred to w here to append, rather than overwrite, values
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open
    pass

filewriter = csv.writer(fnnr_export)
filewriter.writerow(['Step', 'Household ID', 'Individual ID', 'Age', 'Education', 'Marriage', 'Work Status',
                     'Migration Years', 'Past HH ID', 'Migration Network'])

fnnr_export.flush()  # flush memory
fnnr_export.close()

def save(step_counter, hh_id, individual_id, age, education, marriage, workstatus, mig_years, past_hh_id,
         migration_network):
    """Exports entries onto a .csv file"""
    try:
        fnnr_export = open('FNNR-ABM_export.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # a is also preferred to w here to append, rather than overwrite, values
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
        pass
    fnnr_export.writelines(str(step_counter))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(hh_id))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(individual_id))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(age))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(education))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(marriage))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(workstatus))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(mig_years))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(past_hh_id))
    fnnr_export.writelines(',')
    fnnr_export.writelines(str(migration_network))
    fnnr_export.writelines('\n')
    fnnr_export.flush()  # flush memory
    fnnr_export.close()
