# !/usr/bin/python

"""
This document defines agents and its attributes.
It also defines what occurs to the agents at each 'step' of the ABM.
"""

from mesa import Agent  # Agent superclass from mesa
from random import *  # random # generator
from excel_import import *
from math import exp
from excel_export_household import save, save_land

single_male_list = []
married_male_list = []
new_married_list = []
initial_migrants_list = []
household_migrants_list = []
out_migrants_list = []
re_migrants_list = []
birth_list = []
death_list = []
nongtgplist = []
gtgplist = []
hhlist = []
household_income = [0] * 94
birth_flag_list = []
marriage_flag_list = []

class HouseholdAgent(Agent):  # child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, unique_id, model, hh_id,
                 admin_village):

        super().__init__(unique_id, model)
        # self.hhpos = hhpos
        self.model = model
        self.hh_id = hh_id
        self.admin_village = admin_village
        self.nat_village = 1
        try:
            self.hh_row = get_hh_row(int(self.hh_id))
        except:
            if 'k' in self.hh_id:
                self.hh_id = self.hh_id[:self.hh_id.index('k')]
            if 'j' in self.hh_id:
                self.hh_id = self.hh_id[:self.hh_id.index('j')]
            else:
                self.hh_id = self.hh_id[:-1]
            self.hh_row = get_hh_row(int(self.hh_id))
        self.gtgp_enrolled = 0  # binary (GTGP status of household)
        self.income = 0  # will re-set later
        self.mig_prob = 0.5  # migration probability, preset 0.5
        if self.hh_row is not None and self.hh_row <= 94:
            self.num_mig = initialize_migrants(self.hh_row)  # how many migrants the hh has
            self.num_labor = initialize_labor(self.hh_row)
        self.min_req_labor = 1  # preset
        self.gtgp_comp = randint(500, 2000)
        self.comp_sign = 0.1  # influence of GTGP income on migration decisions
        self.gtgp_coef = uniform(0, 0.55)  # compared to mig_prob, which is 0.5, should give ~10% chance of > 0.5
        self.gtgp_part_flag = 0  # binary; further enrollment of GTGP
        self.mig_remittances = return_values(self.hh_row, 'mig_remittances')

        self.first_step_flag = 0
        self.current_year = 2016
        self.step_counter = 0
        if self.hh_row is not None and self.hh_row <= 94:
            try:
                self.hh_size = len(return_values(self.hh_row, 'age'))
            except:
                self.hh_size = 0
        else:
            self.hh_size = 0
        self.migration_network = 0

    def return_labor(self):
        return self.num_labor

    def step(self):
        """Step behavior for household agents; see pseudo-code document"""
        self.current_year += 1
        # if int(self.step_counter) < 5:
        #     save(self.step_counter, self.current_year, self.hh_id, self.num_labor, self.num_mig,
        #          self.hh_size)
        if self.step_counter == 0:
            if self.mig_remittances is not None and int(self.mig_remittances) > 0:
                household_income[self.hh_row - 3] = int(self.mig_remittances)
            else:
                household_income[self.hh_row - 3] = 0
        self.step_counter += 1
        if self.hh_id in hhlist:
            hhlist.remove(self.hh_id)


class LandParcelAgent(HouseholdAgent):
    """Sets land parcel agents; superclass is HouseholdAgent"""

    def __init__(self, unique_id, model, hh_id, hh_row, landpos, gtgp_enrolled, age_1,
                 gender_1, education_1, gtgp_dry, gtgp_rice, total_dry, total_rice, admin_village):

        super().__init__(self, unique_id, hh_id, admin_village)
        self.hh_row = hh_row
        self.landpos = landpos
        self.gtgp_enrolled = gtgp_enrolled
        self.age_1 = age_1
        self.gender_1 = gender_1
        self.education_1 = education_1
        self.land_type = 0
        self.land_time = 0
        self.gtgp_net_income = 0
        self.land_income = 0
        self.plant_type = 0

        self.gtgp_dry = gtgp_dry
        self.gtgp_rice = gtgp_rice
        self.total_dry = total_dry
        self.total_rice = total_rice

        self.non_gtgp_output = 0
        self.pre_gtgp_output = 0
        self.hh_size = 0

        self.step_counter = 0

    def output(self):
        if self.plant_type == 1:
            unit_price = 0.7
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
            land_output = float(self.pre_gtgp_output)
        else:
            land_output = float(self.non_gtgp_output)
        crop_income = land_output * unit_price
        unit_comp = 270  # scenarios at the end of pseudocode
        self.total_rice = return_values(self.hh_row, 'non_gtgp_rice_mu')
        if self.total_rice in ['-3', '-4', -3, None]:
            self.total_rice = 0
        self.total_dry = return_values(self.hh_row, 'non_gtgp_dry_mu')
        if self.total_dry in ['-3', '-4', -3, None]:
            self.total_dry = 0
        self.land_area = float(self.total_dry) + float(self.total_rice)
        comp_amount = self.land_area * unit_comp
        self.gtgp_net_income = comp_amount - crop_income
        self.land_income = comp_amount + crop_income

    def gtgp_participation(self):
        """Initializes labor and determines non-GTGP and GTGP staus"""
        if self.first_step_flag == 0:
            # self.num_labor = self.initialize_labor(self.hh_row)
            self.first_step_flag = 1  # prevents above lines from repeating after initialization
        minimum_non_gtgp = 0.3
        non_gtgp_area = (float(self.total_dry) + float(self.total_rice)) - (float(self.gtgp_dry) + float(self.gtgp_rice))
        if non_gtgp_area < minimum_non_gtgp:
            gtgp_part_prob = 0
        prob = exp(2.52 - 0.012 * self.age_1 - 0.29 * self.gender_1 + 0.01 * self.education_1 + 0.001 * self.hh_size
                   - 2.45 * self.land_type * 0.0006 * self.gtgp_net_income + 0.04 * self.land_time)
        gtgp_part_prob = prob / (prob + 1)
        # self.hh_size = len(return_values(self.hh_row, 'age'))
        # print(self.hh_id, self.age_1, self.gender_1, self.education_1, self.gtgp_enrolled, 'test1')
        # print(self.land_type, self.gtgp_net_income, self.land_time, self.hh_size, 'test')
        if random() < gtgp_part_prob:  # verify
            self.gtgp_enrolled = 1
        return self.gtgp_enrolled

    def non_gtgp_count(self, nongtgplist, gtgplist):
        if self.gtgp_enrolled == 0 and self.unique_id not in nongtgplist:
            if len(nongtgplist) + len(gtgplist) != 722:
                nongtgplist.append(self.unique_id)
            else:
                nongtgplist = []
                nongtgplist.append(self.unique_id)
        return len(nongtgplist)

    def gtgp_count(self, gtgplist, nongtgplist):
        if self.gtgp_enrolled == 1 and self.unique_id not in gtgplist:
            if self.unique_id in nongtgplist:
                nongtgplist.remove(self.unique_id)
            if len(nongtgplist) + len(gtgplist) != 722:
                gtgplist.append(self.unique_id)
            else:
                gtgplist = []
                gtgplist.append(self.unique_id)
        return len(gtgplist)

    def step(self):
        """Step behavior for LandParcelAgent"""
        self.non_gtgp_count(nongtgplist, gtgplist)
        self.gtgp_count(gtgplist, nongtgplist)
        self.output()
        self.gtgp_participation()
        household_income[self.hh_row - 3] = (household_income[self.hh_row - 3]
                                                      + self.land_income)
        #if int(self.step_counter) < 5:
        #    save_land(household_income[self.hh_row - 1])
        self.step_counter += 1


class IndividualAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model, hh_id, individual_id, age, gender, education,
                 marriage, admin_village = 0):

        super().__init__(unique_id, model, hh_id, admin_village)

        self.hh_id = hh_id
        self.individual_id = individual_id
        self.age = age
        self.gender = gender
        self.education = education
        if 15 < self.age < 59:
            self.workstatus = 1
        else:
            self.workstatus = 0
        self.marriage = marriage

        self.birth_rate = 0.0123
        self.birth_interval = 2
        self.birth_flag = 0
        self.death_rate = 0.0077
        self.death_flag = 0
        self.marriage_rate = 0.0087
        self.marriage_flag = 0
        self.match_prob = 0.05
        self.immi_marriage_rate = 0.03
        self.mig_flag = 0
        self.past_hh_id = 0
        self.last_birth_time = 0
        self.mig_years = 0
        self.remittance = 0
        self.husband_id = 0
        self.past_individual_id = 0

        self.step_counter = 0

        self.hh_size = 0
        try:
            self.hh_row = get_hh_row(int(self.hh_id))
        except:
            if 'k' in self.hh_id:
                self.hh_id = self.hh_id[:self.hh_id.index('k')]
            if 'j' in self.hh_id:
                self.hh_id = self.hh_id[:self.hh_id.index('j')]
            else:
                self.hh_id = self.hh_id[:-1]
            self.hh_row = get_hh_row(int(self.hh_id))
        if self.hh_row is not None and self.hh_row <= 96:
            self.num_labor = initialize_labor(int(self.hh_row) - 2)
            self.num_mig = initialize_migrants(int(self.hh_row) - 2)
        self.admin_village = 0
        # print(self.hh_id, self.individual_id, self.age, self.gender, self.education, 'break', self.workstatus,
        #      self.marriage, self.admin_village, self.workstatus, self.marriage, 'test except hhrow')

    def create_initial_migrant_list(self, hh_row):
        self.hh_row = hh_row
        mig = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                              self.education, self.marriage, self.admin_village)
        try:
            mig.age = return_values(self.hh_row, 'initial_migrants')[0]
            mig.gender = return_values(self.hh_row, 'initial_migrants')[1]
            mig.marriage = return_values(self.hh_row, 'initial_migrants')[2]
            mig.education = return_values(self.hh_row, 'initial_migrants')[3]
            mig.mig_years = return_values(self.hh_row, 'initial_migrants')[4]
            mig.individual_id = str(self.hh_id) + 'm'
            # m is the generic individual id letter for initial migrants in the household
            if mig.individual_id not in initial_migrants_list and self.hh_id not in household_migrants_list:
                initial_migrants_list.append(mig.individual_id)
                out_migrants_list.append(mig.individual_id)
                self.schedule.add(mig)
                self.running = True
                # household_migrants_list.append(self.hh_id)
        except: # NoneType; also, migrant in row 15 with -3 education
            pass

    def match_female(self):
        """Loops through single females and matches to single males; see pseudocode"""
        global single_male_list  # debug suggestion: return it at step 0
        if int(self.age) > 20 and self.gender == 1 and self.individual_id not in single_male_list    \
                and self.individual_id not in married_male_list:
            single_male_list.append(self.individual_id)
            shuffle(single_male_list)  # randomizes males to go through
            if self.individual_id in married_male_list:
                self.marriage = 1
        if random() < self.marriage_rate:
            marriage_flag_list.append(1)
        if self.age > 20 and self.gender == 2 and self.marriage != 1   \
            and self.past_individual_id == 0 and 'j' not in self.individual_id  \
            and marriage_flag_list != []:
            # if person is a woman,
            self.past_individual_id = self.individual_id
            self.past_hh_id = self.hh_id
            self.marriage_flag = 1
            self.marriage = 1
            loop = 0
            for male in single_male_list:
                if random() < float(self.match_prob) and loop == 0:
                    married_male_list.append(male)
                    self.husband_id = male
                    if 'k' not in male:
                        self.hh_id = male.strip(male[-1])
                        self.individual_id = self.hh_id + 'j'
                    else:
                        self.hh_id = male[:male.index('k')]
                        self.individual_id = self.hh_id + 'j' + '-' + str(self.step_counter)
                    new_married_list.append(self.individual_id)
                    single_male_list.remove(male)
                    marriage_flag_list.remove(1)
                    loop = 1  # same thing as using a While loop

    def immigration_marriage(self):
        """Adds a 3% chance that an additional immigrant marriage takes place along with a given marriage"""
        if self.marriage_flag == 1 and random() < self.immi_marriage_rate:
            ind = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                                  self.education, self.workstatus, self.marriage, self.birth_rate, self.birth_interval,
                                  self.death_rate, self.marriage_rate, self.marriage_flag, self.mig_flag,
                                  self.match_prob, self.immi_marriage_rate, self.past_hh_id, self.mig_years,
                                  self.hh_row)
            ind.gender = 2
            age_random = normalvariate(22.1, 2.6)
            if age_random >= 20.0:
                ind.age = age_random
            else:
                ind.age = 20
            ind.education = normalvariate(8.7, 1.3)
            ind.marriage = 1
            random_male = choice(single_male_list)
            if self.individual_id == random_male:
                self.marriage = 1
                ind.hh_id = random_male.strip(random_male[-1])
                ind.individual_id = ind.hh_id + 'j'  # j is the generic individual id letter for newly-married females
            ind.workstatus = 1

    def birth(self):
        """Adds a new IndividualAgent class object"""
        birth_rate = 0.01
        if random() < birth_rate:
            birth_flag_list.append(1)
        if self.marriage == 1 and self.gender == 2 and self.age < 55 and birth_flag_list != []:
            if (float(self.step_counter) - float(self.last_birth_time)) > float(self.birth_interval):
                self.last_birth_time = self.step_counter
                if self.hh_id != 'Dead':
                    ind = IndividualAgent(self.hh_id, self, self.individual_id, self.age, self.gender,
                                          self.education, self.workstatus, self.marriage, self.admin_village)
                    ind.age = 0
                    ind.gender = choice([1, 2])
                    ind.education = 0
                    ind.workstatus = 6
                    ind.marriage = 0
                    ind.hh_id = self.hh_id
                    ind.individual_id = str(self.hh_id) + 'k' + '-' + str(self.step_counter)
                    # k is the generic individual id letter for newborn children in the household
                    birth_list.append(ind.individual_id)
                    birth_flag_list.remove(1)
                    try:
                        self.model.schedule.add(ind)
                        self.running = True
                    except:
                        try:
                            self.model.model.schedule.add(ind)
                            self.running = True
                        except:
                            self.model.model.model.schedule.add(ind)
                            self.running = True
                            #if self.past_individual_id is not 0:
                    #    print('success', 'past:',self.past_individual_id, 'ind_id:', self.individual_id,
                    #          'hus:', self.husband_id, self.model, self.step_counter, 'success')
                    #except:
                        #print('fail', 'past:', self.past_individual_id, 'ind_id:',
                        #      self.individual_id, 'hus:', self.husband_id, self.model, self.step_counter, 'fail')
                        #pass

    def death(self):
        """Removes an object from reference"""
        if random() < self.death_rate:
            self.death_flag += 1
        if self.age > 65 and self.death_flag > 0:
                self.hh_id = 'Dead'
                if self.individual_id not in death_list:
                    death_list.append(self.individual_id)
                # self.individual_id = 0
                self.num_mig -= 1
                if self.hh_id in household_migrants_list:
                    household_migrants_list.remove(self.hh_id)
                self.death_flag -= 1

    def youth_education(self):
        """Assigns student working status to those who are young"""
        if 7 < self.age < 19:
            self.workstatus = 5
            # *5 for student education + 1
            # what about after they turn 20?

    # def get_hh_row_agents(self, hh_id):
    #     hh_id = self.hh_id
    #     return get_hh_row(hh_id)

    def out_migration(self):
        """Describes out-migration process and probability"""
        income_local_off_farm = return_values(self.hh_row, 'income_local_off_farm')
        if income_local_off_farm is None:
            income_local_off_farm = 0
        if self.workstatus == 1:
            farm_work = 1  # converts working status into binary farm work status
        else:
            farm_work = 0
        self.mig_flag = 0
        # step 0
        # try:
        #      self.num_labor = super().initialize_labor(self.hh_row)
        # except:
        #      self.num_labor = 0
        # if self.num_labor == None:
        #     self.num_labor = 0

        self.total_rice = return_values(self.hh_row, 'non_gtgp_rice_mu')
        if self.total_rice in ['-3', '-4', -3, None]:
            self.total_rice = 0
        self.total_dry = return_values(self.hh_row, 'non_gtgp_dry_mu')
        if self.total_dry in ['-3', '-4', -3, None]:
            self.total_dry = 0
        self.gtgp_dry = return_values(self.hh_row, 'gtgp_dry_mu')
        if self.gtgp_dry in ['-3', '-4', -3, None]:
            self.gtgp_dry = 0
        self.gtgp_rice = return_values(self.hh_row, 'gtgp_rice_mu')
        if self.gtgp_rice in ['-3', '-4', -3, None]:
            self.gtgp_rice = 0
        if self.num_labor != 0 and self.num_labor is not None:
            non_gtgp_area = (float(self.total_rice) + float(self.total_dry))    \
                            - (float(self.gtgp_dry) + float(self.gtgp_rice))
            non_GTGP_land_per_labor = non_gtgp_area / self.num_labor
        else:
            non_GTGP_land_per_labor = 0
        if self.hh_id != 'Dead' and self.hh_id != 'Migrated' and self.hh_id is not None:
            try:
                self.migration_network = return_values(self.hh_row, 'migration_network')
            except:
                self.migration_network = 0
        else:
             self.migration_network = 0
        if self.migration_network == None:
             self.migration_network = 0
        remittance = normalvariate(1200, 16000)
        if remittance < 0:
            remittance = 0
        self.remittance = float(remittance)
        prob = exp(2.07 - 0.00015 * float(income_local_off_farm) + 0.67 * float(self.num_labor)
                   + 4.36 * float(self.migration_network) - 0.58 * float(non_GTGP_land_per_labor)
                   + 0.27 * float(self.gtgp_enrolled) - 0.13 * float(self.age) + 0.07 * float(self.gender)
                   + 0.17 * float(self.education) + 0.88 * float(self.marriage) +
                   1.39 * float(farm_work) + 0.001 * float(self.remittance))
        if prob > 1:
            prob = 1
        mig_prob = prob / (prob + 1)
        self.hh_size = len(return_values(int(self.hh_row - 2), 'age'))
        if random() < mig_prob and self.hh_size >= 2:
            if self.hh_id not in household_migrants_list:  # only 1 migrant at a time per hh
                self.mig_flag = 1
                self.num_mig += 1
                if 15 < self.age < 65 and self.num_labor > 1:
                    self.num_labor -= 1
                self.hh_size -= 1
                self.past_hh_id = self.hh_id
                if self.hh_id not in household_migrants_list:
                    household_migrants_list.append(self.hh_id)
                if self.individual_id not in out_migrants_list:
                    out_migrants_list.append(self.individual_id)
                self.hh_id = 'Migrated'
                self.workstatus = 4
                if self.individual_id in re_migrants_list:
                    re_migrants_list.remove(self.individual_id)

    def re_migration(self):
        """Describes re-migration process and probability following out-migration"""
        if self.individual_id in out_migrants_list:
            # prob = exp(5.31 - 0.12 * self.age + 0.14 * self.mig_years)
            # old formula above
            self.mig_years += 1
            prob = exp(-1.2 + 0.06 * self.age - 0.08 * self.mig_years)
            # age is defined as the age at the time of migration
            if prob > 1:
                prob = 1
            re_mig_prob = prob / (prob + 1)
            if random() < re_mig_prob:
                self.remittances = 0
                self.hh_id = self.past_hh_id
                self.workstatus = 1
                #out_migrants_list.remove(self.individual_id)
                if self.individual_id not in re_migrants_list:
                    re_migrants_list.append(self.individual_id)
                self.hh_size += 1
                self.num_mig -= 1
                if self.hh_id in household_migrants_list:
                    household_migrants_list.remove(self.hh_id)
                if 15 < self.age < 65:
                    self.num_labor += 1


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
            self.age += 1
        household_income[self.hh_row - 3] = (household_income[self.hh_row - 3]
                                                      + self.remittance)
        # self.step_counter = int(self.step_counter)
        if int(self.step_counter) < 5:
            # can change 5 to any number of steps, but code will take longer to run
            # selects one individual to represent the household
            if str(self.individual_id)[-1] == 'a' and self.hh_id != 'Dead'  \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    save(self.step_counter, self.current_year, self.individual_id[:-1], self.num_labor, self.num_mig,
                         self.hh_size, household_income[self.hh_row - 3])
            elif str(self.individual_id)[-1] == 'b' and self.hh_id != 'Dead'  \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    save(self.step_counter, self.current_year, self.individual_id[:-1], self.num_labor, self.num_mig,
                        self.hh_size, household_income[self.hh_row - 3])
            elif str(self.individual_id)[-1] == 'c' and self.hh_id != 'Dead' \
                and (self.gender == 1 or self.marriage == 0) \
                and self.hh_id != 'Migrated' and self.hh_id not in hhlist:
                    hhlist.append(self.hh_id)
                    save(self.step_counter, self.current_year, self.individual_id[:-1], self.num_labor, self.num_mig,
                        self.hh_size, household_income[self.hh_row - 3])
        self.current_year += 1
        self.step_counter += 1
        self.first_step_flag = 1  # must be at the end of step()

