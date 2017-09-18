# !/usr/bin/python

"""
If you are new to this project, start reading code here.
This document defines agents and its attributes.
It also defines what occurs to the agents at each 'step' of the ABM.
"""

from mesa import Agent  # Agent superclass from mesa
from random import *  # random # generator
from excel_import import *
from excel_import_2014 import *
from math import exp
from excel_export_household import save
from excel_export_household_2014 import save_2014

single_male_list = []
married_male_list = []
new_married_list = []
initial_migrants_list = []
household_migrants_list = []
out_migrants_list = []
re_migrants_list = []
birth_list = []
death_list = []
birth_flag_list = []
marriage_flag_list = []
death_flag_list = []
nongtgplist = []
gtgplist = []
gtgp_part_list = []
hhlist = []


# each index represents a household
cumulative_mig_list = [0] * 94
cumulative_re_mig_list = [0] * 94
re_mig_list = [0] * 94
out_mig_list = [0] * 94
num_labor_list = [0] * 94
hh_size_list = [0] * 94
household_income_list = [0] * 94

single_male_list_2014 = []
married_male_list_2014 = []
new_married_list_2014 = []
initial_migrants_list_2014 = []
household_migrants_list_2014 = []
out_migrants_list_2014 = []
re_migrants_list_2014 = []
birth_list_2014 = []
death_list_2014 = []
birth_flag_list_2014 = []
marriage_flag_list_2014 = []
death_flag_list_2014 = []
nongtgplist_2014 = []
gtgplist_2014 = []
hhlist_2014 = []

cumulative_mig_list_2014 = [0] * 20
cumulative_re_mig_list_2014 = [0] * 20
re_mig_list_2014 = [0] * 20
out_mig_list_2014 = [0] * 20
num_labor_list_2014 = [0] * 20
hh_size_list_2014 = [0] * 20
household_income_list_2014 = [0] * 20

class HouseholdAgent(Agent):  # child class of Mesa's generic Agent class
    """Sets household data, including initial values"""
    def __init__(self, unique_id, model, hh_id, admin_village):

        super().__init__(unique_id, model)
        self.hh_id = hh_id
        self.admin_village = admin_village

        try:
            self.hh_row = get_hh_row(int(self.hh_id)) - 2
            # household ids go from 1-169; household row refers to the Excel file, 1-94
        except:  # just in case an error sets individual ids as household ids
            if self.hh_id.islower() == False:
                self.hh_row = get_hh_row(int(self.hh_id)) - 1
            elif 'k' in self.hh_id:  # k is the tag for the second generation of people
                self.hh_id = self.hh_id[:self.hh_id.index('k')]
            elif 'j' in self.hh_id:  # j is a generic married-woman tag
                self.hh_id = self.hh_id[:self.hh_id.index('j')]
            else:
                self.hh_id = self.hh_id[:-1]
            self.hh_row = get_hh_row(int(self.hh_id)) - 2
        # if self.hh_row <= 94:
        #     self.out_mig = initialize_migrants(self.hh_row)  # how many migrants the hh has
        #     self.num_labor = initialize_labor(self.hh_row) # how many laborers the hh has
#        if self.hh_row <= 94:
#             self.mig_remittances = return_values(self.hh_row, 'mig_remittances') # remittances of initial migrant

        self.first_step_flag = 0
        self.hh_step_counter = 0

        # self.hh_size = len(return_values(self.hh_row, 'age'))
        # else:
        #     self.hh_size = 0

    def return_labor(self):
        #return self.num_labor
        return num_labor_list[self.hh_row - 1]

    def step(self):
        """Step behavior for household agents; see pseudo-code document"""
 #       if self.mig_remittances is not None and int(self.mig_remittances) > 0   \
 #           and self.hh_step_counter == 0:
#                household_income_list[self.hh_row - 1] = int(self.mig_remittances)
        # print(self.hh_step_counter, household_income_list)
        self.hh_step_counter += 1
        if self.hh_id in hhlist:  # used for Excel file import later in this document
            hhlist.remove(self.hh_id) # resets list every step


class LandParcelAgent(Agent):
    """Sets land parcel agents; superclass is HouseholdAgent"""

    def __init__(self, unique_id, model, hh_id, hh_row, landpos, gtgp_enrolled, age_1,
                 gender_1, education_1, gtgp_dry, gtgp_rice, total_dry, total_rice,
                 land_type, land_time, plant_type, non_gtgp_output, pre_gtgp_output):

        super().__init__(unique_id, model)
        self.hh_id = hh_id
        self.hh_row = hh_row
        self.landpos = landpos  # coordinate form
        self.gtgp_enrolled = gtgp_enrolled  # inherited from HouseholdAgent
        self.age_1 = age_1  # calculated in model.py
        self.gender_1 = gender_1
        self.education_1 = education_1
        self.land_type = land_type
        self.land_time = land_time
        self.gtgp_net_income = 0  # calculated later
        self.land_income = 0  # calculated later
        self.plant_type = plant_type
        # print(self.hh_row, self.landpos, self.gtgp_enrolled, self.age_1, self.gender_1, self.education_1)

        self.gtgp_dry = gtgp_dry  # calculated in model.py
        self.gtgp_rice = gtgp_rice
        self.total_dry = total_dry
        self.total_rice = total_rice
        # print(self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice)

        self.non_gtgp_output = non_gtgp_output
        self.pre_gtgp_output = pre_gtgp_output

        self.land_step_counter = 0

    def output(self):
        """Calculates land output and income"""
        if self.plant_type == 1:
            unit_price = 0.7  # set in pseudo-code
        elif self.plant_type == 2:
            unit_price = 0.8
        elif self.plant_type == 3:
            unit_price = 0.9
        elif self.plant_type == 4:
            unit_price = 2.3
        elif self.plant_type == 5:
            unit_price = 0
        else:
            unit_price = 1
        if self.gtgp_enrolled == 1:
            try:
                land_output = float(self.pre_gtgp_output)
            except ValueError:
                pass
        else:
            land_output = float(self.non_gtgp_output)
        crop_income = land_output * unit_price

        unit_comp = 270  # scenarios at the end of pseudocode

        if self.landpos != 0:
            self.total_rice = return_values(self.hh_row, 'non_gtgp_rice_mu')
            if self.total_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.total_dry = return_values(self.hh_row, 'non_gtgp_dry_mu')
            if self.total_dry in ['-3', '-4', -3, None]:
                self.total_dry = 0
        else:
            self.total_rice = return_values_2014(self.hh_row, 'non_gtgp_rice_mu')
            if self.total_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.total_dry = return_values_2014(self.hh_row, 'non_gtgp_dry_mu')
            if self.total_dry in ['-3', '-4', -3, None]:
                self.total_dry = 0
        self.land_area = float(self.total_dry) + float(self.total_rice)
        comp_amount = self.land_area * unit_comp
        self.gtgp_net_income = comp_amount - crop_income
        self.land_income = comp_amount + crop_income


    def gtgp_participation(self):
        """Initializes labor and determines non-GTGP and GTGP status"""
        minimum_non_gtgp = 0.3  # set in pseudo-code
        if self.total_dry == None:  # not applicable to 2014 data
            self.total_dry = 0
        if self.total_rice == None:
            self.total_rice = 0
        if self.gtgp_dry == None:
            self.gtgp_dry = 0
        if self.gtgp_rice == None:
            self.gtgp_rice = 0
        non_gtgp_area = (float(self.total_dry) + float(self.total_rice)) - (float(self.gtgp_dry) + float(self.gtgp_rice))
        self.hh_size = len(return_values(self.hh_row, 'age'))
        try:
            prob = exp(2.52 - 0.012 * float(self.age_1) - 0.29 * float(self.gender_1) + 0.01 * float(self.education_1)
                   + 0.001 * float(self.hh_size) - 2.45 * self.land_type * 0.0006 * float(self.gtgp_net_income)
                   + 0.04 * self.land_time)
        except:
            prob = 0
            pass
        if non_gtgp_area < minimum_non_gtgp:
            gtgp_part_prob = 0
        gtgp_part_prob = prob / (prob + 1)
        if random() < gtgp_part_prob:
            self.gtgp_enrolled = 1
            if self.hh_id not in gtgp_part_list:
                # print(len(gtgp_part_list))
                gtgp_part_list.append(self.hh_id)
        return self.gtgp_enrolled

    def non_gtgp_count(self, nongtgplist, gtgplist):
        """Counts non-GTGP land parcels for graphing"""
        if self.gtgp_enrolled == 0 and self.landpos != 0 and self not in nongtgplist and self not in gtgplist:
            nongtgplist.append(self)

    def gtgp_count(self, nongtgplist, gtgplist):
        """Counts GTGP land parcels for graphing"""
        if self.gtgp_enrolled == 1 and self in nongtgplist and self not in gtgplist:
            nongtgplist.remove(self)
            gtgplist.append(self)

    def non_gtgp_count_2014(self, nongtgplist_2014, gtgplist_2014):
        """Counts non-GTGP land parcels for graphing"""
        if self.gtgp_enrolled == 0 and self.landpos == 0 and self not in nongtgplist_2014 and self not in gtgplist_2014:
            nongtgplist_2014.append(self)

    def gtgp_count_2014(self, nongtgplist_2014, gtgplist_2014):
        """Counts GTGP land parcels for graphing"""
        if self.gtgp_enrolled == 1 and self not in gtgplist_2014 and self in nongtgplist_2014:
            nongtgplist_2014.remove(self)
            gtgplist_2014.append(self)

    def step(self):
        """Step behavior for LandParcelAgent"""
        old_land_income = self.land_income  # resets yearly?
        self.non_gtgp_count(nongtgplist, gtgplist)
        self.gtgp_count(nongtgplist, gtgplist)
        self.non_gtgp_count_2014(nongtgplist_2014, gtgplist_2014)
        self.gtgp_count_2014(nongtgplist_2014, gtgplist_2014)
        self.output()
        self.gtgp_participation()
        # print(self.land_step_counter, self.hh_row, self.landpos, self.land_income, old_land_income)
        if self.landpos != 0:
            household_income_list[self.hh_row - 1] = (household_income_list[self.hh_row - 1]
                                              + self.land_income - old_land_income)
        elif self.landpos == 0 and self.hh_row < 22:
            household_income_list_2014[self.hh_row - 3] = (household_income_list_2014[self.hh_row - 3]
                                                        + self.land_income - old_land_income)
        self.land_step_counter += 1


class IndividualAgent(Agent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model, hh_id, individual_id, age, gender, education,
                 marriage, past_hh_id, non_gtgp_area, step_counter, age_at_step_0, income_local_off_farm):

        super().__init__(unique_id, model)

        self.hh_id = hh_id
        self.individual_id = str(individual_id)
        self.age = age
        self.income_local_off_farm = income_local_off_farm
        self.age_at_step_0 = age_at_step_0

        self.gender = gender
        self.education = education
        if 15 < self.age < 59:
            self.workstatus = 1
        else:
            self.workstatus = 0
        self.marriage = marriage
        self.non_gtgp_area = non_gtgp_area

        self.birth_rate = 0.0121  # changeable
        self.birth_interval = 2
        self.birth_flag = 0
        self.death_rate = 0.0072  # changeable
        self.death_flag = 0
        self.marriage_rate = 0.007  # changeable
        self.marriage_flag = 0
        self.match_prob = 0.05  # pre-set from pseudo-code
        self.immi_marriage_rate = 0.03  # pre-set from pseudo-code

        self.mig_flag = 0
        self.past_hh_id = past_hh_id
        self.last_birth_time = 0
        self.mig_years = 0

        self.work_flag = 0
        self.retire_flag = 0

        self.husband_id = 0  # for testing purposes
        self.past_individual_id = 0


        if '2014' not in self.individual_id:
            try:  # in case individual ids get assigned as household ids
                self.hh_row = get_hh_row(int(self.hh_id)) - 2
            except:
                if 'k' in self.hh_id:  # second-generation
                    self.hh_id = self.hh_id[:self.hh_id.index('k')]
                if 'j' in self.hh_id:  # married women
                    self.hh_id = self.hh_id[:self.hh_id.index('j')]
                else:
                    self.hh_id = self.hh_id[:-1]
                self.hh_row = get_hh_row(int(self.hh_id))

        elif '2014' in self.individual_id:
            try:
                self.hh_row = get_hh_row_2014(int(self.hh_id)) - 2
            except ValueError:
                self.hh_id = self.hh_id[:-6]
                self.hh_row = get_hh_row_2014(int(self.hh_id)) - 2
        self.step_counter = 0

        if '2014' not in self.individual_id and self.hh_row <= 94:
            self.hh_size = len(return_values(int(self.hh_row), 'age'))
        elif '2014' in self.individual_id and self.hh_row <= 94:
            self.hh_size = len(return_values_2014(int(self.hh_row + 1), 'age'))

        if type(self.individual_id) == str:
            if '2014' not in self.individual_id:
                self.current_year = 2016
            else:
                self.current_year = 2014

        if self.hh_row is not None and self.hh_row <= 94 and '2014' not in self.individual_id:
            self.num_labor = initialize_labor(int(self.hh_row))
            self.out_mig = initialize_migrants(int(self.hh_row))
        elif '2014' in self.individual_id and self.hh_row <= 20:
            self.num_labor = initialize_labor_2014(int(self.hh_row) + 2)
            self.out_mig = initialize_migrants_2014(int(self.hh_row) + 2)
        else:
            self.num_labor = 0
            self.out_mig = 0

        try:
            if '2014' not in self.individual_id:
                self.migration_network = return_values(self.hh_row, 'migration_network')
            elif '2014' in self.individual_id:
                self.migration_network = return_values_2014(self.hh_row + 2, 'migration_network')
        except:
            self.migration_network = 0
        if self.migration_network == None:
             self.migration_network = 0

    def create_initial_migrant_list(self, hh_row):
        """Creates a list of initial migrants from exported data"""
        self.hh_row = hh_row
        mig = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                              self.education, self.marriage, self.past_hh_id, self.non_gtgp_area, self.step_counter,
                              self.age_at_step_0, self.income_local_off_farm)
        try:
            if '2014' not in self.individual_id:
                mig.age = return_values(self.hh_row, 'initial_migrants')[0]
                mig.gender = return_values(self.hh_row, 'initial_migrants')[1]
                mig.marriage = return_values(self.hh_row, 'initial_migrants')[2]
                mig.education = return_values(self.hh_row, 'initial_migrants')[3]
                mig.mig_years = return_values(self.hh_row, 'initial_migrants')[4]
                mig.individual_id = str(self.hh_id) + 'm'
                mig.remittance = normalvariate(1200, 16000)
                if mig.remittance < 0:
                    mig.remittance = 0
                mig.past_hh_id = str(self.hh_id)
                # m is the generic individual id letter for initial migrants in the household
                if mig.individual_id not in initial_migrants_list and self.hh_id not in household_migrants_list:
                    initial_migrants_list.append(mig.individual_id)
                    out_migrants_list.append(mig.individual_id)
                    out_mig_list[self.hh_row - 1] += 1
                    household_migrants_list.append(self.hh_id)
                    self.schedule.add(mig)
                    self.running = True
            else:
                mig.age = return_values_2014(self.hh_row, 'initial_migrants')[0]
                mig.gender = return_values_2014(self.hh_row, 'initial_migrants')[1]
                mig.marriage = return_values_2014(self.hh_row, 'initial_migrants')[2]
                mig.education = return_values_2014(self.hh_row, 'initial_migrants')[3]
                mig.mig_years = return_values_2014(self.hh_row, 'initial_migrants')[4]
                mig.individual_id = str(self.hh_id) + 'm' + '_' + '2014'
                mig.past_hh_id = str(self.hh_id)
                # m is the generic individual id letter for initial migrants in the household
                if mig.individual_id not in initial_migrants_list_2014 and self.hh_id not in household_migrants_list:
                    initial_migrants_list_2014.append(mig.individual_id)
                    out_migrants_list_2014.append(mig.individual_id)
                    out_mig_list_2014[self.hh_row - 1] += 1
                    self.schedule.add(mig)
                    self.running = True
                # household_migrants_list.append(self.hh_id)
        except: # NoneType; also, valid migrant in row 15 of data with -3 education
            pass

    def match_female(self):
        """Loops through single females and matches to single males; see pseudo-code"""

        if self.marriage != 1:
            self.past_hh_id = 0

        global single_male_list
        # live-update single_male_list to accommodate for males born since the beginning of the model
        if int(self.age) > 20 and self.gender == 1 and self.individual_id not in single_male_list    \
                and self.individual_id not in married_male_list and '2014' not in self.individual_id    \
                and self.individual_id not in out_migrants_list and self.hh_id != 0 and self.marriage != 1:
                    single_male_list.append(self.individual_id)
                    shuffle(single_male_list)  # randomizes males to go through

        # 2014 version
        elif int(self.age) > 20 and self.gender == 1 and self.individual_id not in single_male_list    \
                and self.individual_id not in married_male_list and '2014' in self.individual_id    \
                and self.individual_id not in out_migrants_list_2014 and self.hh_id != 0 and self.marriage != 1:
                    single_male_list_2014.append(self.individual_id)
                    shuffle(single_male_list_2014)  # randomizes males to go through

        if self.individual_id in married_male_list or self.individual_id in married_male_list_2014:
            self.marriage = 1

        if random() < self.marriage_rate:
            marriage_flag_list.append(1)
            marriage_flag_list_2014.append(1)#

        # if self.gender == 2 and '2014' in self.individual_id:
        #     print(self.age, self.marriage)

        if int(self.age) > 20 and int(self.gender) == 2 and int(self.marriage) != 1:
            if 'j' not in self.individual_id  \
                and self.individual_id not in out_migrants_list \
                    and self.individual_id not in out_migrants_list_2014 and marriage_flag_list != []:
                    # if person is a previously-unmarried, non-migrated woman,


                    self.past_individual_id = self.individual_id
                    self.past_hh_id = self.hh_id
                    self.marriage = 1
                    self.marriage_flag = 0
                    if '2014' not in self.individual_id:
                        for male in single_male_list:
                            if random() < float(self.match_prob) and self.marriage_flag == 0:
                                self.marriage_flag = 1
                                married_male_list.append(male)
                                self.husband_id = male
                                if 'k' not in male:
                                    self.hh_id = male.strip(male[-1])
                                    if self.hh_id != 0:
                                        new_married_list.append(self.individual_id)
                                        self.individual_id = self.hh_id + 'j'
                                else:
                                    self.hh_id = male[:male.index('k')]
                                    self.individual_id = self.hh_id + 'j' + '-' + str(self.step_counter)
                                    new_married_list.append(self.individual_id)
                                single_male_list.remove(male)
                                marriage_flag_list.remove(1)
                    elif '2014' in self.individual_id:
                        for male in single_male_list_2014:
                            if random() < float(self.match_prob) and self.marriage_flag == 0:
                                married_male_list_2014.append(male)
                                self.husband_id = male
                                if 'k' not in male:
                                    self.hh_id = male.strip(male[-6])
                                    self.individual_id = self.hh_id + 'j'
                                    new_married_list_2014.append(self.individual_id)
                                else:
                                    self.hh_id = male[:male.index('k')]
                                    self.individual_id = self.hh_id + 'j' + '-' + str(self.step_counter) + '_2014'
                                    new_married_list_2014.append(self.individual_id)
                                single_male_list_2014.remove(male)
                                marriage_flag_list_2014.remove(1)
                                self.marriage_flag = 1

    def immigration_marriage(self):
        """Adds a 3% chance that an additional immigrant marriage takes place along with a given marriage"""
        if self.marriage_flag == 1 and random() < self.immi_marriage_rate:
            ind = IndividualAgent(self.hh_id, self, self.individual_id, self.age, self.gender,
                                  self.education, self.workstatus, self.marriage, self.admin_village,
                                  self.step_counter, self.age_at_step_0, self.income_local_off_farm)
            ind.gender = 2
            age_random = normalvariate(22.1, 2.6)  # see pseudo-code
            if age_random >= 20.0:
                ind.age = age_random
            else:
                ind.age = 20
            ind.education = normalvariate(8.7, 1.3)  # see pseudo-code
            ind.marriage = 1
            random_male = choice(single_male_list)
            if self.individual_id == random_male:
                self.marriage = 1
                ind.hh_id = random_male.strip(random_male[-1])
                ind.individual_id = ind.hh_id + 'j'  # j is the generic individual id letter for newly-married females
            ind.workstatus = 1

    def birth(self):
        """Adds a new IndividualAgent class object"""
        if random() < self.birth_rate:
            birth_flag_list.append(1)
        if self.marriage == 1 and self.gender == 2 and self.age < 55    \
            and birth_flag_list != []:
            if (float(self.step_counter) - float(self.last_birth_time)) > float(self.birth_interval):
                self.last_birth_time = self.step_counter
                self.hh_size += 1
                self.age_at_step_0 = 0
                ind = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                                      self.education, self.marriage, self.past_hh_id, self.non_gtgp_area, self.step_counter,
                                      self.age_at_step_0, self.income_local_off_farm)
                ind.age = 0
                ind.gender = choice([1, 2])
                ind.education = 0
                ind.workstatus = 6
                ind.marriage = 0
                ind.hh_id = self.hh_id
                ind.step_counter = self.step_counter

                if '2014' not in self.individual_id:
                    ind.individual_id = str(self.hh_id) + 'k' + '-' + str(self.step_counter)
                # k is the generic individual id letter for newborn children in the household
                elif '2014' in self.individual_id:
                    ind.individual_id = str(self.hh_id) + 'k' + '-' + str(self.step_counter) + '_2014'
                if '2014' not in self.individual_id:
                    birth_list.append(ind.individual_id)
                    hh_size_list[self.hh_row - 1] += 1
                elif '2014' in self.individual_id:
                    birth_list_2014.append(ind.individual_id)
                    hh_size_list_2014[self.hh_row - 1] += 1
                birth_flag_list.remove(1)

                try:
                    self.model.schedule.add(ind)
                    self.running = True
                except:
                    try:
                        self.model.model.schedule.add(ind)
                        self.running = True
                    except:
                        try:
                            self.model.model.model.schedule.add(ind)
                            self.running = True
                        except:
                            self.model.model.model.model.schedule.add(ind)
                            self.running = True


    def death(self):
        """Removes an object from reference"""
        if random() < self.death_rate:
            death_flag_list.append(1)
        if int(self.age) > 65 and self.individual_id not in out_migrants_list and death_flag_list != []:
                self.hh_id = 'Dead'
                if '2014' not in self.individual_id:
                    death_list.append(self.individual_id)
                    hh_size_list[self.hh_row - 1] -= 1
                elif '2014' in self.individual_id:
                    death_list_2014.append(self.individual_id)
                    hh_size_list_2014[self.hh_row - 1] -= 1
                # self.individual_id = 0
                self.hh_size -= 1

                self.num_labor -= 1  # no retirement in pseudo-code

                death_flag_list.remove(1)

                if self.individual_id in re_migrants_list:
                    re_migrants_list.remove(self.individual_id)
                    re_mig_list[self.hh_row - 1] -= 1
                elif self.individual_id in re_migrants_list_2014:
                    re_migrants_list_2014.remove(self.individual_id)
                    re_mig_list_2014[self.hh_row - 1] -= 1


    def youth_education(self):
        """Assigns student working status to those who are young"""
        if 7 < int(self.age) < 19:
            self.workstatus = 5
            # what about after they turn 20?

    def aging(self):
        if self.age > 19 and self.workstatus == 5:
            self.workstatus = 1
        if self.age_at_step_0 <= 19 and self.age >= 20 and self.work_flag == 0:  # join the workforce
            self.num_labor += 1
            if '2014' not in self.individual_id:
                num_labor_list[self.hh_row - 1] += 1
            elif '2014' in self.individual_id:
                num_labor_list_2014[self.hh_row - 1] += 1
            self.work_flag = 1  # can only add to labor numbers once
        if self.age_at_step_0 <= 64 and self.age >= 65 and self.retire_flag == 0:  # retire
            if '2014' not in self.individual_id:
                self.num_labor -= 1
                num_labor_list[self.hh_row - 1] -= 1
            elif '2014' in self.individual_id:
                self.num_labor -= 1
                num_labor_list_2014[self.hh_row - 1] -= 1
            self.retire_flag = 1  # can only retire once

    def out_migration(self):
        """Describes out-migration process and probability"""

        if '2014' not in self.individual_id and self.hh_row <= 94:
            try:
                self.income_local_off_farm = float(return_values(self.hh_row, 'income_local_off_farm'))
            except TypeError:  # None
                pass
            if self.income_local_off_farm == None:
                self.income_local_off_farm = 0
        elif '2014' in self.individual_id:
            if self.hh_id == 31:
                self.income_local_off_farm = (float(7500))
            elif self.hh_id == 39:
                self.income_local_off_farm = (float(12000))
            elif self.hh_id == 57:
                self.income_local_off_farm = (float(18000))
            elif self.hh_id == 148:
                self.income_local_off_farm = (float(9600))
            elif self.hh_id == 153:
                self.income_local_off_farm = (float(600))
            else:
                self.income_local_off_farm = 0
        else:
            self.income_local_off_farm = 0
        if self.workstatus == 1:
            farm_work = 1  # converts working status into binary farm work status
        else:
            farm_work = 0
        self.mig_flag = 0
        if '2014' not in self.individual_id and self.hh_row <= 94:

            self.total_rice = return_values(self.hh_row + 1, 'non_gtgp_rice_mu')
            if self.total_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.total_dry = return_values(self.hh_row + 1, 'non_gtgp_dry_mu')
            if self.total_dry in ['-3', '-4', -3, None]:
                self.total_dry = 0
            self.gtgp_dry = return_values(self.hh_row + 1, 'gtgp_dry_mu')
            if self.gtgp_dry in ['-3', '-4', -3, None]:
                self.gtgp_dry = 0
            self.gtgp_rice = return_values(self.hh_row + 1, 'gtgp_rice_mu')
            if self.gtgp_rice in ['-3', '-4', -3, None]:
                self.gtgp_rice = 0

            non_gtgp_area = (float(self.total_rice) + float(self.total_dry)) \
                            - (float(self.gtgp_dry) + float(self.gtgp_rice))

            if num_labor_list[self.hh_row - 1] != 0:
                non_GTGP_land_per_labor = non_gtgp_area / num_labor_list[self.hh_row - 1]
            else:
                non_GTGP_land_per_labor = 0

        elif '2014' in self.individual_id and self.hh_row <= 94:
            non_gtgp_area = self.non_gtgp_area
            if num_labor_list_2014[self.hh_row - 1] != 0:
                non_GTGP_land_per_labor = non_gtgp_area / num_labor_list_2014[self.hh_row - 1]
            else:
                non_GTGP_land_per_labor = 0

        else:
            non_gtgp_area = 0

        remittance = normalvariate(1200, 16000)
        if remittance < 0:
            remittance = 0
        self.remittance = float(remittance)
        if self.hh_id in gtgp_part_list:
            self.gtgp_part = 1
        else:
            self.gtgp_part = 0
        if self.hh_id not in household_migrants_list and self.individual_id not in out_migrants_list:
            #print(income_local_off_farm, self.migration_network, self.gtgp_part, farm_work, self.remittance,
            #      non_GTGP_land_per_labor, self.education, self.remittance, farm_work)
            prob = exp(2.07 - 0.00015 * float(self.income_local_off_farm) + 0.67 * float(self.num_labor)
                       + 4.36 * float(self.migration_network) - 0.58 * float(non_GTGP_land_per_labor)
                       + 0.27 * float(self.gtgp_part) - 0.13 * float(self.age) + 0.07 * float(self.gender)
                       + 0.17 * float(self.education) + 0.88 * float(self.marriage) +
                       1.39 * float(farm_work) + 0.001 * float(self.remittance))
            mig_prob = prob / (prob + 1)
            if random() < mig_prob and self.hh_size >= 2 and self.hh_id not in household_migrants_list  \
                    and self.hh_id not in household_migrants_list_2014:  # out-migration occurs
                        if '2014' not in self.individual_id:
                            # print(self.step_counter, self.hh_row, self.hh_id, self.individual_id, self.remittance)
                            household_income_list[self.hh_row - 1] = (household_income_list[self.hh_row - 1]
                                                                 + self.remittance)
                            out_mig_list[self.hh_row - 1] += 1
                            cumulative_mig_list[self.hh_row - 1] += 1
                            hh_size_list[self.hh_row - 1] -= 1

                        elif '2014' in self.individual_id and self.hh_row < 22:
                            # print(self.step_counter, self.hh_row, self.hh_id, self.individual_id, self.remittance)
                            household_income_list_2014[self.hh_row - 1] = (household_income_list_2014[self.hh_row - 1]
                                                                      + self.remittance)
                            out_mig_list_2014[self.hh_row - 1] += 1
                            cumulative_mig_list_2014[self.hh_row - 1] += 1
                            hh_size_list_2014[self.hh_row - 1] -= 1
                        self.hh_size -= 1

                        self.past_hh_id = self.hh_id
                        self.workstatus = 4
                        self.out_mig += 1


                        if 15 < int(self.age) < 65 and self.num_labor > 1:
                            self.mig_flag = 1
                            self.num_labor -= 1
                            if '2014' not in self.individual_id:
                                num_labor_list[self.hh_row - 1] -= 1
                            elif '2014' in self.individual_id:
                                num_labor_list_2014[self.hh_row - 1] -= 1

                        if '2014' not in self.individual_id:
                            household_migrants_list.append(self.hh_id)
                            out_migrants_list.append(self.individual_id)
                            if self.individual_id in re_migrants_list:
                                re_migrants_list.remove(self.individual_id)
                                re_mig_list[self.hh_row - 1] -= 1

                        elif '2014' in self.individual_id:
                            if self.hh_id not in household_migrants_list_2014:
                                household_migrants_list_2014.append(self.hh_id)
                            if self.individual_id not in out_migrants_list_2014:
                                out_migrants_list_2014.append(self.individual_id)
                            if self.individual_id in re_migrants_list_2014:
                                re_migrants_list_2014.remove(self.individual_id)
                                re_mig_list_2014[self.hh_row - 1] -= 1
                        self.hh_id = 'Migrated'

    def re_migration(self):
        """Describes re-migration process and probability following out-migration"""
        if self.step_counter == 0 and '2014' in self.individual_id:
            self.mig_remittances = household_income_list[self.hh_row - 1]
            # else:
            #     self.mig_remittances = household_income_list[self.hh_row - 1]
#        if (self.individual_id in out_migrants_list or self.individual_id in out_migrants_list_2014)  \
#            and (self.hh_id in household_migrants_list or self.hh_id in household_migrants_list_2014):
        if self.hh_id == 'Migrated':
                self.mig_years += 1

                prob = exp(-1.2 + 0.06 * float(self.age) - 0.08 * self.mig_years)
                re_mig_prob = prob / (prob + 1)
                if random() < re_mig_prob:
                    self.mig_years = 0
                    if '2014' not in self.individual_id:
                        if 'm' in self.individual_id:
                            self.mig_remittances = return_values(self.hh_row,
                                                                 'mig_remittances')  # remittances of initial migrant                    if 'm' in self.individual_id:
                            household_income_list[self.hh_row - 1] = household_income_list[self.hh_row - 1] \
                                                                - float(self.mig_remittances)
                        else:
                            household_income_list[self.hh_row - 1] = household_income_list[self.hh_row - 1]\
                                                                - self.remittance

                    elif '2014' in self.individual_id and self.hh_row < 22:
                        if 'm' in self.individual_id:
                            self.mig_remittances = return_values(self.hh_row,
                                                                 'mig_remittances')
                            if self.mig_remittances is None:
                                self.mig_remittances = 0
                            household_income_list_2014[self.hh_row - 1] = household_income_list_2014[self.hh_row] \
                                                            - float(self.mig_remittances)
                        else:
                            household_income_list_2014[self.hh_row - 1] = household_income_list_2014[self.hh_row - 1] \
                                                                - self.remittance
                    self.hh_id = self.past_hh_id
                    self.workstatus = 1
                    if self.individual_id in out_migrants_list:
                        out_migrants_list.remove(self.individual_id)
                    elif self.individual_id in out_migrants_list_2014:
                        out_migrants_list_2014.remove(self.individual_id)
                    if self.individual_id not in re_migrants_list and '2014' not in self.individual_id:
                        re_migrants_list.append(self.individual_id)
                        re_mig_list[self.hh_row - 1] += 1
                        cumulative_re_mig_list[self.hh_row - 1] += 1
                    elif self.individual_id not in re_migrants_list_2014 and '2014' in self.individual_id:
                        re_migrants_list_2014.append(self.individual_id)
                        re_mig_list_2014[self.hh_row - 1] += 1
                        cumulative_re_mig_list_2014[self.hh_row -1] += 1

                    self.hh_size += 1
                    self.out_mig -= 1

                    if '2014' not in self.individual_id:
                        hh_size_list[self.hh_row - 1] += 1
                        out_mig_list[self.hh_row - 1] -= 1
                    elif '2014' in self.individual_id and self.hh_row < 22:
                        hh_size_list_2014[self.hh_row - 1] += 1
                        out_mig_list_2014[self.hh_row - 1] -= 1

                    if self.hh_id in household_migrants_list:
                        household_migrants_list.remove(self.hh_id)
                    elif self.hh_id in household_migrants_list_2014:
                        household_migrants_list_2014.remove(self.hh_id)

                    if 15 < int(self.age) < 65:
                        self.num_labor += 1
                        if '2014' not in self.individual_id:
                            num_labor_list[self.hh_row - 1] += 1
                        elif '2014' in self.individual_id:
                            num_labor_list_2014[self.hh_row - 1] += 1


    def step(self):
        """Step behavior for individual agents; calls above functions"""
        if self.hh_id != 'Migrated' and self.hh_id != 'Dead':
            self.match_female()
            self.birth()
            self.death()
            self.youth_education()
            self.out_migration()
        if self.hh_id != 'Dead':
            self.re_migration()
            self.age = float(self.age)
            self.age += 1
        if self.step_counter == 0 and '2014' not in self.individual_id:
            household_income_list[self.hh_row - 1] = household_income_list[self.hh_row - 1] + self.income_local_off_farm
        elif self.step_counter == 0 and '2014' in self.individual_id:
            household_income_list_2014[self.hh_row - 1] = household_income_list_2014[self.hh_row - 1] + self.income_local_off_farm


        # self.step_counter = int(self.step_counter)
        if int(self.step_counter) < 5:
            # can change 5 to any number of steps, but code will take longer to run
            # selects one individual to represent the household in calculating hh size, etc.
            if str(self.individual_id)[-1] == 'a' and self.hh_id != 'Dead'  \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    if '2014' not in self.individual_id:
                        save(self.step_counter, self.current_year, self.hh_id,
                             num_labor_list[self.hh_row - 1], out_mig_list[self.hh_row - 1],
                             hh_size_list[self.hh_row - 1], household_income_list[self.hh_row - 1])
            elif str(self.individual_id)[-1] == 'b' and self.hh_id != 'Dead'  \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    save(self.step_counter, self.current_year, self.hh_id,
                         num_labor_list[self.hh_row - 1], out_mig_list[self.hh_row - 1],
                         hh_size_list[self.hh_row - 1], household_income_list[self.hh_row - 1])
            elif str(self.individual_id)[-1] == 'c' and self.hh_id != 'Dead' \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    save(self.step_counter, self.current_year, self.hh_id,
                         num_labor_list[self.hh_row - 1], out_mig_list[self.hh_row - 1],
                         hh_size_list[self.hh_row - 1], household_income_list[self.hh_row - 1])
            elif '2014' in self.individual_id and self.hh_id != 'Dead' \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated':
                    save_2014(self.step_counter, self.current_year, self.hh_id,
                            num_labor_list_2014[self.hh_row], out_mig_list_2014[self.hh_row],
                            hh_size_list_2014[self.hh_row], household_income_list_2014[self.hh_row])

        self.current_year += 1
        self.step_counter += 1
        self.first_step_flag = 1  # must be at the end of step()

