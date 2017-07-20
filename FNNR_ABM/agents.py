# !/usr/bin/python

"""
This document defines agents and its attributes.
It also defines what occurs to the agents at each 'step' of the ABM.
"""

from mesa import Agent  # Agent superclass from mesa
from random import *  # random # generator
from excel_import import *
from math import sqrt, exp
from excel_export_individual import save


formermax = []
single_male_list = []
married_male_list = []
out_migrants_list = []
re_migrants_list = []
birth_list = []
death_list = []
hhlist = []
nongtgplist = []
gtgplist = []


class HouseholdAgent(Agent):  # child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, unique_id, model, hhpos, hh_id, admin_village = 1, nat_village = 1, land_area = 100,
                 charcoal = 10, gtgp_dry = 50, gtgp_rice = 50, total_dry = 50, total_rice = 50,
                 NCFP = 1, num_mig = 0, income = 0, mig_prob = 0.5, num_labor = 0, num_non_labor = 0,
                 min_req_labor = 1, comp_sign = 0.1, gtgp_coef = 0, gtgp_part = 0, gtgp_part_flag = 0,
                 gtgp_comp = 0, first_step_flag = 0, restaurant_prev = 0, lodging_prev = 0,
                 transport_prev = 0, sales_prev = 0, other_prev = 0, current_year = 2016, migration_network = 0,
                 age_1 = 0, gender_1 = 0, education_1 = 0):

        super().__init__(unique_id, model)
        self.hhpos = hhpos  # resident location
        self.hh_id = hh_id
        self.admin_village = admin_village
        self.nat_village = nat_village
        self.charcoal = charcoal  # consumption
        self.land_area = land_area  # total land area for household
        self.gtgp_dry = gtgp_dry  # area
        self.gtgp_rice = gtgp_rice  # area
        self.total_dry = total_dry  # area
        self.total_rice = total_rice  # area
        self.NCFP = NCFP  # another PES program
        self.num_mig = num_mig  # how many migrants the hh has

        self.gtgp_part = gtgp_part  # binary (GTGP status of household)
        self.income = randint(5000, 20000)  # yearly household income
        self.mig_prob = mig_prob  # migration probability, preset 0.5
        self.num_labor = num_labor  # people in hh who can work, preset to 15-65
        self.num_non_labor = num_non_labor  # people in hh whose ages are < 15 or > 65
        self.min_req_labor = min_req_labor  # preset
        self.gtgp_comp = randint(500, 2000)
        self.comp_sign = comp_sign  # influence of GTGP income on migration decisions
        self.gtgp_coef = uniform(0, 0.55)  # compared to mig_prob, which is 0.5, should give ~10% chance of > 0.5
        self.gtgp_part_flag = gtgp_part_flag  # binary; further enrollment of GTGP

        self.first_step_flag = first_step_flag
        self.current_year = current_year
        # more attributes will be added later on

        self.restaurant_prev = restaurant_prev
        self.lodging_prev = lodging_prev
        self.transport_prev = transport_prev
        self.sales_prev = sales_prev
        self.other_prev = other_prev
        self.migration_network = migration_network

        self.age_1 = age_1
        self.gender_1 = gender_1
        self.education_1 = education_1

    def return_labor(self):
        return self.num_labor

    def initialize_labor(self, hh_row):
        num_labor = 0
        # There are 94 total households, but ids range from 1-169.
        # for clarity: hh_row refers to the Excel spreadsheet row, 3-96 (representing 94 households).
        # hh_id refers to household ids as assigned in the Excel column, numbering from 1-169.
        agelist = return_values(hh_row, 'age')  # find the ages of people in hh
        if agelist is not None:  # if there are people in the household,
            for age in agelist:  # for each person (can't use self.age because not a Household-level attribute),
                try:
                    # ages are strings by default, must convert to float
                    if 15 < float(age) < 59:  # if the person is 15-65 years old,
                        num_labor += 1  # defines number of laborers as people aged 15 < x < 59
                    elif 0 < float(age) < 15 and float(age) > 59:
                        self.num_non_labor += 1  # defines non-laborers, may not necessarily be used
                except:
                    pass  # covers situations in which age is 'NoneType'
            return num_labor

    def gtgp_participation(self):
        minimum_non_gtgp = 0.3
        non_gtgp_area = (self.total_dry + self.total_rice) - (self.gtgp_dry + self.gtgp_rice)
        if non_gtgp_area < minimum_non_gtgp:
            gtgp_part_prob = 0
        # Ask Shuang


    def step(self):
        """Step behavior for household agents; see pseudo-code document"""
        # use either self.gtgp_test() or self.gtgp_enroll()
        self.current_year += 1

    # def gtgp_enroll(self):
    #     # self.num_mig = real_value_counter(return_values(self.unique_id, 'num_mig')) / 17  # sets num_mig in hh
    #     # 17: 1999-2016, so num_mig is average yearly number of migrants per household
    #     # if self.first_step_flag == 0:
    #     #   laborchance = randint(1,6)
    #     #     self.num_labor = laborchance  # initialize number of laborers randomly
    #     if self.first_step_flag == 0:
    #         # unique_id here is hh_row from model.py, line 176
    #         if self.initialize_labor(self.unique_id) is not None and type(self.unique_id) == int:
    #             self.num_labor = self.initialize_labor(self.unique_id)
    #             self.first_step_flag = 1  # prevents above lines from repeating after initialization
    #     self.gtgp_part = 1
    #     # later: depends on plant type and land area and PES policy
    #     self.gtgp_coef = uniform(0, 0.55)  # numbers taken from pseudocode
    #     self.gtgp_comp = randint(500, 2000)
    #     self.income = randint(5000, 20000)
    #     if type(self.unique_id) == int and self.hh_id is not None:
    #         if (self.gtgp_coef * self.gtgp_part) > self.mig_prob and (self.gtgp_comp / self.income) > self.comp_sign:
    #             if self.num_labor > 0:
    #                 self.num_labor -= 1
    #                 self.num_mig += 1  # migration occurs
    #                 # print(' # of laborers: ', self.num_labor, ' # of migrants: ', self.num_mig)
    #             if self.num_labor < self.min_req_labor and int(self.hh_id) not in hhlist:
    #                 gtgp_part_flag = 1  # sets flag for enrollment of more land
    #                 hhlist.append(int(self.hh_id))
    #     return hhlist  # a list of households set to enroll in further GTGP; see LandParcelAgent's gtgp_convert()

    # def gtgp_test(self):
    #     # Basic formula for testing web browser simulation; each step, 5% of agents change flags.
    #     # can remove function once model is finished; just for debugging purposes / template for future functions
    #     if self.first_step_flag == 0:
    #         self.num_labor = self.initialize_labor(self.unique_id)
    #     if self.num_labor > 0:
    #         self.num_labor -= 1
    #         self.num_mig += 1
    #         # print(' # of laborers: ', self.num_labor, ' # of migrants: ', self.num_mig)
    #     chance = random()
    #     if chance > 0.95:
    #         self.gtgp_part_flag = 1


class IndividualAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model, hh_id, individual_id, age = 20, gender = 1, education = 1,
                 workstatus = 0, marriage = 0, birth_rate = 1, birth_interval = 2, death_rate = 0.1,
                 marriage_rate = 0.1, marriage_flag = 0, mig_flag = 0, match_prob = 0.05, immi_marriage_rate = 0.03,
                 past_hh_id = 0, last_birth_time = 0, mig_years = 0, remittance_prev = 0, step_counter = 0,
                 num_mig = 1, num_labor = 1):

        super().__init__(self, unique_id, model, hh_id, num_mig, num_labor)
        self.individual_id = individual_id
        self.hh_id = self.individual_id[:-1]  # for example, if individual id is 94f, household id is 94
        self.age = age
        self.gender = gender
        self.education = education
        self.workstatus = workstatus

        self.marriage = marriage
        self.birth_rate = birth_rate
        self.birth_interval = birth_interval
        self.death_rate = death_rate
        self.marriage_rate = marriage_rate
        self.marriage_flag = marriage_flag
        self.match_prob = match_prob
        self.immi_marriage_rate = immi_marriage_rate
        self.mig_flag = mig_flag
        self.past_hh_id = past_hh_id
        self.last_birth_time = last_birth_time
        self.mig_years = mig_years
        self.remittance_prev = remittance_prev

        self.step_counter = step_counter

    def match_female(self):
        """Loops through single females and matches to single males; see pseudocode"""
        self.marriage_flag = 0
        if self.first_step_flag == 0:
            global single_male_list  # debug suggestion: return it at step 0
            if 20 < self.age and self.gender == 1:
                single_male_list.append(self.individual_id)
                shuffle(single_male_list)  # randomizes males to go through
        # agelist = return_values(self.hh_id, 'age')  # find the ages of people in hh
        # genderlist = return_values(self.hh_id, 'gender')
        if self.marriage != 1:
            self.marriage = 0  # set default to 0
            if 20 < self.age and self.gender == 2 and self.marriage == 0:
                # if person is a woman,
                if random() < self.marriage_rate:
                    for male in single_male_list:
                        if random() < self.match_prob:
                            self.marriage_flag = 1
                            self.marriage = 1
                            married_male_list.append(male)
                            self.hh_id = male.strip(male[-1])
                            self.individual_id = self.hh_id + 'j'
                            single_male_list.remove(male)
                            pass
        # if agelist is not None and genderlist is not None:  # if there are people in the household,
            # for i in range(len(agelist)):  # for each person,
        if 20 < self.age and self.gender == 1:
            if self.individual_id in married_male_list:
                self.marriage = 1

    def immigration_marriage(self):
        """Adds a 3% chance that an additional immigrant marriage takes place along with a given marriage"""
        if self.marriage_flag == 1 and random() < self.immi_marriage_rate:
            ind = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                                  self.education, self.workstatus, self.marriage, self.birth_rate, self.birth_interval,
                                  self.death_rate, self.marriage_rate, self.marriage_flag, self.mig_flag,
                                  self.match_prob, self.immi_marriage_rate, self.past_hh_id, self.mig_years)
            ind.gender = 2
            age_random = normal(22.1, 2.6)
            if age_random >= 20.0:
                ind.age = age_random
            else:
                ind.age = 20
            ind.education = normal(8.7, 1.3)
            ind.marriage = 1
            random_male = choice(single_male_list)
            if self.individual_id == random_male:
                self.marriage = 1
                ind.hh_id = random_male.strip(random_male[-1])
                ind.individual_id = ind.hh_id + 'j'  # j is the generic individual id letter for newly-married females
            ind.workstatus = 1

    def birth(self):
        """Adds a new IndividualAgent class object"""
        if self.marriage == 1 and self.gender == 2 and self.age < 55 and random() < self.birth_rate:
            if random() > self.birth_rate and (self.mig_years - self.last_birth_time) > self.birth_interval:
                self.last_birth_time = self.mig_years
                if self.hh_id != 0:
                    ind = IndividualAgent(self.hh_id, self, self.hh_id, self.individual_id, self.age, self.gender,
                                          self.education, self.workstatus, self.marriage, self.birth_rate,
                                          self.birth_interval, self.death_rate, self.marriage_rate, self.marriage_flag,
                                          self.mig_flag, self.match_prob, self.immi_marriage_rate, self.past_hh_id,
                                          self.last_birth_time, self.mig_years)
                    ind.age = 0
                    ind.gender = choice([0, 1])
                    ind.education = 0
                    ind.marriage = 0
                    ind.individual_id = str(self.hh_id) + 'k'
                    # k is the generic individual id letter for newborn children in the household
                    # change later in case more children are botn
                    ind.workstatus = 6
                    birth_list.append(ind.individual_id)
                    # (birth_list)
        # self.mig_years += 1
        # the above was line in pseudocode, but should not be in this function
        # add to schedule

    def death(self):
        """Removes an object from reference"""
        if self.age > 65 and random() < self.death_rate:
            self.hh_id = '0'
            death_list.append(self.individual_id)
            self.individual_id = '0'

    def youth_education(self):
        """Assigns student working status to those who are young"""
        if 7 < self.age < 19:
            self.workstatus = 5
            # *5 for student education + 1
            # what about after they turn 20?

    def out_migration(self):
        """Describes out-migration process and probability"""
        if self.workstatus == 1 or self.workstatus == 2:
            farm_work = 1  # converts working status into binary farm work status
        else:
            farm_work = 0
        self.mig_flag = 0
        if self.num_labor != 0:
            non_gtgp_area = (self.total_dry + self.total_rice) - (self.gtgp_dry + self.gtgp_rice)
            non_GTGP_land_per_labor = non_gtgp_area / self.num_labor
        else:
            non_GTGP_land_per_labor = 0
        # mig_prob = 0  # pseudocode said to set to 0 initially, but not needed
        migration_network = 0  # temporary
        prob = exp(2.07 + 0.65 * self.num_labor + 4.35 * migration_network +
                   0.11 * non_GTGP_land_per_labor + 0.36 * self.gtgp_part - 0.12 * self.age +
                   0.25 * self.gender + 0.13 * self.education + 0.96 * self.marriage +
                   0.01 * farm_work)
        if prob > 1:
            prob = 1
        mig_prob = prob / (prob + 1)
        if random() < mig_prob:
            self.mig_flag = 1
            # self.num_mig? Ask Shuang
            self.past_hh_id = self.hh_id
            self.hh_id = 0
            out_migrants_list.append(self.individual_id)
            self.workstatus = 4

    def re_migration(self):
        """Describes re-migration process and probability following out-migration"""
        if self.individual_id in out_migrants_list:
            # prob = exp(5.31 - 0.12 * self.age + 0.14 * self.mig_years)
            # old formula above
            self.mig_years += 1
            prob = exp(-1.2 + 0.06 * self.age - 0.08 * self.mig_years)
            # age is defined as the age at the time of migration
            re_mig_prob = prob / (prob + 1)
            if random() < re_mig_prob:
                self.hh_id = self.past_hh_id
                self.workstatus = 1
                out_migrants_list.remove(self.individual_id)
                re_migrants_list.append(self.individual_id)

    def step(self):
        """Step behavior for individual agents; calls above functions"""
        if self.step_counter < 5:
            save(self.step_counter, self.current_year, self.hh_id, self.individual_id, self.age, self.education,
                 self.marriage, self.workstatus, self.mig_years, self.past_hh_id, self.num_mig, self.return_labor())
        self.match_female()
        self.birth()
        self.death()
        self.youth_education()
        self.out_migration()
        self.re_migration()
        self.age += 1
        self.current_year += 1
        self.first_step_flag = 1  # must be at the end of step()
        self.step_counter += 1

class LandParcelAgent(HouseholdAgent):
    """Sets land parcel agents; superclass is HouseholdAgent"""

    def __init__(self, unique_id, model, hhpos, hh_id, landpos, gtgp_enrolled = 0, area = 1, latitude = 0,
                 longitude = 0, maximum = 0, plant_type = 1, land_output = 0, land_type = 0, land_time = 0,
                 gtgp_net_income = 0):

        super().__init__(self, unique_id, model, hhpos, hh_id)
        self.hh_id = hh_id
        self.landpos = landpos
        self.gtgp_enrolled = gtgp_enrolled
        self.area = area
        self.latitude = latitude
        self.longitude = longitude
        self.plant_type = plant_type
        self.land_output = land_output
        self.land_type = land_type
        self.land_time = land_time
        self.maximum = maximum
        self.gtgp_net_income = gtgp_net_income

    def calc_distance(self, hhpos):
        """Given a household id, return the distances between household and parcels"""
        landpos = self.landpos
        if hhpos is not None:
            try:
                distance = sqrt(
                    (landpos[0] - hhpos[0]) ** 2 + (landpos[1] - hhpos[1]) ** 2
                    )
            except:
                pass
        try:
            if distance < 10:
                return distance
        except:
            pass

    def determine_hhpos_agents(self, hh_id, latitude, longitude):
        """Determine position of agent on map"""
        try:
            x = convert_fraction_lat(
                convert_decimal(
                    str(return_values(hh_id, latitude))
                )
            )[0] * 10

            y = convert_fraction_long(
                convert_decimal(
                    str(return_values(hh_id, longitude))
                )
            )[0] * 10
            pos = (x, y)
            return pos
        except:
            pass

    def recalculate_max(self):
        """Every step, returns new max-distance land parcel for each household given households and land parcels"""
        maxlist = []
        hhpos = self.determine_hhpos_agents(self.hh_id, 'house_latitude', 'house_longitude')
        distance = self.calc_distance(hhpos)
        if distance not in formermax:
            maxlist.append(distance)
            formermax.append(distance)
        if maxlist != ['']:
            try:
                self.maximum = 1
            except:
                self.maximum = 0
                pass
        return self.maximum

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
        crop_income = self.land_output * unit_price
        unit_comp = 1  # preset, not in pseudocode currently
        comp_amount = self.land_area * unit_comp
        self.gtgp_net_income = comp_amount - crop_income

    def gtgp_part(self):
        if self.land_type == 1:
            prob = exp(1.02 - 0.15 * self.age_1 - 0.07 * self.gender_1 + 0.18 * self.education_1
                       - 0.58 * self.land_time - 0.76 * non_gtgp_land_per_labor + 0.08 * self.gtgp_net_income)
            gtgp_part_prob = prob / (prob + 1)
        else:
            prob = exp(1.24 - 0.16 * self.age_1 - 0.07 * self.gender_1 + 0.12 * self.education_1
                       - 0.23 * self.land_time - 0.85 * non_gtgp_land_per_labor + 0.12 * self.gtgp_net_income)
            gtgp_part_prob = prob / (prob + 1)
        if random() > gtgp_part_prob:
            self.gtgp_enrolled = 1

    # def gtgp_convert(self):
    #     result = super(LandParcelAgent, self).gtgp_enroll()
    #     if int(self.hh_id) in result:
    #         self.gtgp_enrolled = 1

    def non_gtgp_count(self):
        if self.gtgp_enrolled == 0 and self.unique_id not in nongtgplist:
            nongtgplist.append(self.unique_id)
        return len(nongtgplist)

    def gtgp_count(self):
        if self.gtgp_enrolled == 1 and self.unique_id not in gtgplist:
            if self.unique_id in nongtgplist:
                nongtgplist.remove(self.unique_id)
            gtgplist.append(self.unique_id)
        return len(gtgplist)

    def step(self):
        """Step behavior for LandParcelAgent"""
        self.recalculate_max()
        self.non_gtgp_count()
        self.gtgp_count()