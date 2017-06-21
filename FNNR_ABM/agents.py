# !/usr/bin/python

"""
This document defines agents and its attributes.
It also defines what occurs to the agents at each 'step' of the ABM.
"""

from mesa import Agent  # Agent superclass from mesa
from random import *
from excel_import import *
from math import sqrt

formermax = []
class HouseholdAgent(Agent):  # child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, unique_id, model, hhpos, hh_id, admin_village = 1, nat_village = 1, land_area = 100,
                 charcoal = 10, GTGP_dry = 50, GTGP_rice = 50, total_dry = 50, total_rice = 50,
                 NCFP = 1, num_mig = 0, income = 0, mig_prob = 0.5, num_labor = 0,
                 min_req_labor = 1, comp_sign = 0.1, GTGP_coef = 0, GTGP_part = 0, GTGP_part_flag = 0,
                 num_non_labor = 0, GTGP_comp = 0, first_step_flag = 0, birth_rate = 1, birth_interval = 2,
                 death_rate = 0.1, marriage_rate = 0.1, marriage_flag = 0, match_prob = 0.05, immi_marriage_rate = 0.03):

        super().__init__(unique_id, model)  # unique_id = household id
        self.hhpos = hhpos  # resident location
        self.hh_id = hh_id
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
        self.income = randint(5000, 20000)  # yearly household income
        self.mig_prob = mig_prob  # migration probability, preset 0.5
        self.num_labor = num_labor  # people in hh who can work, preset to 15-65
        self.num_non_labor = num_non_labor  # people in hh whose ages are <15 or >65
        self.min_req_labor = min_req_labor  # preset
        self.GTGP_comp = randint(500, 2000)
        self.comp_sign = comp_sign  # influence of GTGP income on migration decisions
        self.GTGP_coef = uniform(0, 0.55)  # random coefficient
        self.GTGP_part_flag = GTGP_part_flag #binary; further enrollment of GTGP
        self.first_step_flag = first_step_flag
        # more attributes will be added later on

        self.birth_rate = birth_rate
        self.birth_interval = birth_interval
        self.death_rate = death_rate
        self.marriage_rate = marriage_rate
        self.marriage_flag = marriage_flag
        self.match_prob = match_prob
        self.immi_marriage_rate = immi_marriage_rate

    def initialize_labor(self, hh):
        num_labor = 0
        agelist = return_values(hh, 'age')  # find the ages of people in hh
        if agelist[0] is not None:  # if there are people in the household,
            for age in agelist:  # for each person,
                try:
                    if 15 < float(age) < 59:  # if the person is 15-65 years old,
                        # if return_values(i,'GTGP_area') != 'None' and return_values(i, 'GTGP_area') != '[]':
                        num_labor += 1  # defines number of laborers as people aged 15 < x < 59
                    # elif 0 < float(age) < 15 and float(age) > 59:
                        # self.num_non_labor += 1
                except:
                    pass  # covers situations in which age is 'NoneType'
            print(num_labor,'num_labor')
            return num_labor

    def gtgp_enroll(self):
        """See pseudo-code document: predicts GTGP participation per household"""
        #for hh in agents: # for each household - removed
        #    self.num_mig = real_value_counter(return_values(hh, 'num_mig')) / 17  # sets num_mig in hh
        # 17: 1999-2016, so num_mig is average yearly number of migrants per household
        #if self.num_labor == 0 and self.charcoal == 10:
       #     laborchance = randint(1,6)
       #     self.num_labor = laborchance  # initialize number of laborers randomly
        if self.first_step_flag == 0:
            if type(self.unique_id) == int:
                # initialize number of laborers
                self.hh_id = self.unique_id
                if self.hh_id > 0:
                    self.num_labor = self.initialize_labor(self.hh_id)
                    #except:
                    #    pass
        print(self.hh_id,'hhid',self.num_labor,'!') #current prob: num_labor outside loop for hh not landparcel
        self.first_step_flag = 1
        try:
            self.GTGP_part = 1
                # break  # avoid redundant flagging
        except:
            pass

        # later: depends on plant type and land area and PES policy
        if type(self.unique_id) == int:
            if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp / self.income) > self.comp_sign:
                try:
                    if self.num_labor > 0:
                        self.num_labor -= 1
                        self.num_mig += 1  # migration occurs
                        print(' # of laborers: ', self.num_labor, ' # of migrants: ', self.num_mig)
                    #pass
                #if self.num_labor == 0 and self.num_non_labor == 0:
                    #break
                except:
                    pass
                if self.num_labor < self.min_req_labor:
                    self.GTGP_part_flag = 1  # sets flag for enrollment of more land
            return self.GTGP_part_flag

    def gtgp_test(self):
        """Basic formula for testing web browser simulation; each step, 5% of agents change flags"""
        try:
            if self.first_step_flag == 0:
                self.num_labor = self.initialize_labor(self.unique_id)
        except:
            pass
        self.first_step_flag = 1
        try:
            if self.num_labor > 0:
                self.num_labor -= 1
                self.num_mig += 1
                print(' # of laborers: ', self.num_labor, ' # of migrants: ', self.num_mig)
        except:
            pass
        chance = random()
        if chance > 0.95:
            self.GTGP_part_flag = 1

    def step(self):
        """Step behavior for household agents; see pseudo-code document"""
        self.admin_village = 1
        self.gtgp_enroll()

# class CommunityAgent(Agent):
    # will set attributes later on

class IndividualAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model):
        super().__init__(self, unique_id, model, hh, age = 20, gender = 1, education = 1,
                         labor = 0, marriage = 0)
        self.age = age
        self.gender = gender
        self.education = education
        self.labor = labor
        self.marriage = marriage

class LandParcelAgent(HouseholdAgent):
    """Sets land parcel agents; superclass is HouseholdAgent"""
    def __init__(self, unique_id, model, hhpos, hh_id, landpos, GTGP_enrolled = 0,
                 area = 1, latitude = 0, longitude = 0, maximum = 0, plant_type = 1):

        super().__init__(self, unique_id, model, hhpos, hh_id)
        self.landpos = landpos
        self.GTGP_enrolled = GTGP_enrolled
        self.area = area
        self.latitude = latitude
        self.longitude = longitude
        self.plant_type = plant_type
        self.maximum = maximum

    def calc_distance(self, hhpos, landpos):
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
                convert_lat_long(
                    str(return_values(hh_id, latitude))
                )
            )[0] * 10

            y = convert_fraction_long(
                convert_lat_long(
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
        # print(hhpos,';;', self.landpos,'!!')
        #try:
        distance = self.calc_distance(hhpos, self.landpos)
        if distance not in formermax:
            maxlist.append(distance)
            formermax.append(distance)
        #except:
        #    pass
        if maxlist != ['']:
            try:
                #max_index = maxlist.index(max(maxlist))
                #if self.landpos == maxlist[max_index]:
                self.maximum = 1
                #else:
                    #self.maximum = 0
            except:
                self.maximum = 0
                pass
        return self.maximum

    def gtgp_convert(self):
        super(LandParcelAgent, self).gtgp_enroll()
        # print(self.GTGP_part_flag,'flag')
        if self.GTGP_part_flag == 1:  # if the household is set to enroll in GTGP,
            if self.maximum == 1:
                self.GTGP_enrolled = 1
            else:
                pass
                #print('work on it')

    def step(self):
        """Step behavior for LandParcelAgent"""
        self.recalculate_max()
        self.gtgp_convert()

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model, GTGP_comp):
        super().__init__(policy_id, model)
        self.GTGP_comp = GTGP_comp
        # more attributes will be added later on
