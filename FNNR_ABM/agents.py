# !/usr/bin/python

"""
This document defines agents and its attributes.
It also defines what occurs to the agents at each 'step' of the ABM.
"""

from mesa import Agent  # Agent superclass from mesa
from random import *
from excel_import import *


class HouseholdAgent(Agent):  # child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, unique_id, model, hhpos, admin_village = 1, nat_village = 1, land_area = 100,
                 charcoal = 10, GTGP_dry = 50, GTGP_rice = 50, total_dry = 50, total_rice = 50,
                 NCFP = 1, num_mig = 0, income = 100, mig_prob = 0.5, num_labor = 0,
                 min_req_labor = 1, comp_sign = 0.1, GTGP_coef = 0, GTGP_part = 0, GTGP_part_flag = 0):

        super().__init__(unique_id, model)  # unique_id = household id
        self.hhpos = hhpos  # resident location
        self.admin_village = admin_village
        self.nat_village = nat_village
        self.charcoal = charcoal # consumption
        self.land_area = land_area  # total land area for household
        self.GTGP_dry = GTGP_dry  # area
        self.GTGP_rice = GTGP_rice # area
        self.total_dry = total_dry  # area
        self.total_rice = total_rice  # area
        self.NCFP = NCFP  # another PES program
        self.num_mig = num_mig  # how many migrants the hh has

        self.GTGP_part = GTGP_part  # binary (GTGP status of household)
        self.income = income  # yearly household income
        self.mig_prob = mig_prob  # migration probability, preset 0.5
        self.num_labor = num_labor  # people in hh who can work, preset to 15-65
        self.min_req_labor = min_req_labor  # preset
        self.comp_sign = comp_sign  # influence of GTGP income on migration decisions
        self.GTGP_coef = GTGP_coef  # randomly generated
        self.GTGP_part_flag = GTGP_part_flag #binary; further enrollment of GTGP
        # more attributes will be added later on

    def gtgp_enroll(self):
        """See pseudo-code document: predicts GTGP participation per household"""
        for hh in agents: # for each household,
            #self.num_mig = convert_num_mig(return_values(hh, 'num_mig')) / 17  # sets num_mig in hh
            # 17: 1999-2016, so num_mig is average yearly number of migrants per household
            if self.num_labor == 0 and self.income == 100:
                laborchance = randint(1,6)
                self.num_labor = laborchance  # initialize number of laborers
            #agelist = return_values(hh, 'age')  # find the ages of people in hh
            #if agelist[0] is not None:  # if there are people in the household,
            #    for age in agelist:  # for each person,
            #        try:
            #            if 15 < float(age) < 59:  # if the person is 15-65 years old,
            #                # if return_values(i,'GTGP_area') != 'None' and return_values(i, 'GTGP_area') != '[]':
            #                self.num_labor += 1  # defines number of laborers as people aged 15 < x < 65
            #        except:
            #            pass  # covers situations in which age is 'NoneType'
            #print(self.num_labor, 'laborers')  # test
            try:
                if return_values(hh, 'GTGP_area')[0] is not '' or None:
                    self.GTGP_part = 1
                    # break  # avoid redundant flagging
            except:
                pass
            self.GTGP_coef = uniform(0, 0.55)  # random coefficient
            compchance = randint(500, 2000)
            self.GTGP_comp = compchance  # calculated later
            incomechance = randint(5000, 20000)
            self.income = incomechance
            # later: depends on plant type and land area and PES policy
            if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp / self.income) > self.comp_sign:
                if self.num_labor > 0:
                    self.num_labor -= 1
                    self.num_mig += 1  # migration occurs
                    # print(hh, ' # of laborers: ', self.num_labor, ' # of migrants: ', self.num_mig)
                    break
                if self.num_labor < self.min_req_labor:
                    self.GTGP_part_flag = 1  # sets flag for enrollment of more land
        return self.GTGP_part_flag

    def gtgp_test(self):
        """Basic formula for testing web browser simulation; each step, 5% of agents change flags"""
        chance = random()
        if chance > 0.95:
            self.GTGP_part_flag = 1

    def step(self):
        """Step behavior for household agents; see pseudo-code document"""
        self.admin_village = 1
#        self.gtgp_enroll()

# class CommunityAgent(Agent):
    # will set attributes later on

class IndividualAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model):
        super().__init__(self, unique_id, model, age = 20, gender = 1, education = 1)
        self.age = age
        self.gender = gender
        self.education = education

class LandParcelAgent(HouseholdAgent):
    """Sets land parcel agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model, landpos, GTGP_enrolled = 0,
                 area = 1, latitude = 0, longitude = 0, maximum = 0, plant_type = 1):

        super().__init__(self, unique_id, model)
        self.landpos = landpos
        self.GTGP_enrolled = GTGP_enrolled
        self.area = area
        self.latitude = latitude
        self.longitude = longitude
        self.plant_type = plant_type
        self.maximum = maximum

    def gtgp_convert(self):
        super(LandParcelAgent, self).gtgp_enroll()
        if self.GTGP_part_flag == 1:  # if the household is set to enroll in GTGP,
            if self.maximum == 1:
                #print('this is the case')
                self.GTGP_enrolled = 1
            else:
                pass
                #print('work on it')

    def step(self):
        """Step behavior for LandParcelAgent"""
        self.gtgp_convert()

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model, GTGP_comp):
        super().__init__(policy_id, model)
        self.GTGP_comp = GTGP_comp
        # more attributes will be added later on
