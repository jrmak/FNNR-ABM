from mesa import Agent #Agent superclass from mesa
import random
from FNNR_ABM.excel_import import *

class HouseholdAgent(Agent):  #child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, hh_id, model, pos, admin_village = 1, nat_village = 1, land_area = 100,
                 charcoal = 10, GTGP_dry = 50, GTGP_rice = 50, total_dry = 50, total_rice = 50,
                 NCFP = 1, num_mig = 1, GTGP_part = 0, income = 100,
                 mig_prob = 0.5, num_labor = 20, min_req_labor = 10, comp_sign = 0.1,
                 GTGP_coef = 0, GTGP_part_flag = 0):

        super().__init__(hh_id, model)
        self.pos = pos  #resident location
        self.admin_village = admin_village
        self.nat_village = nat_village
        self.charcoal = charcoal #consumption
        self.land_area = land_area  #total land area for household
        self.GTGP_dry = GTGP_dry  #area
        self.GTGP_rice = GTGP_rice #area
        self.total_dry = total_dry  #area
        self.total_rice = total_rice  #area
        self.NCFP = NCFP  #another PES program
        self.num_mig = num_mig  #how many migrants the hh currently has

        self.GTGP_part = GTGP_part  #binary (GTGP status of household)
        self.income = income  #yearly household income
        self.mig_prob = mig_prob  #migration probability, preset 0.5
        self.num_labor = num_labor  #people in hh who can work, preset to 15-65
        self.min_req_labor = min_req_labor  #preset
        self.comp_sign = comp_sign  #influence of GTGP income on migration decisions
        self.GTGP_coef = GTGP_coef  #randomly generated
        self.GTGP_part_flag = GTGP_part_flag  #binary; indicates further enrollment
        #more attributes will be added later on

    def gtgp_change(self):
        """See pseudo-code document: predicts GTGP participation per household"""
        for hh in hh_id_list:  #for each household,
            agelist = return_values(hh, 'age')  #find the ages of people in hh
            for age in agelist: #for each person,
                try:
                    if 15 < float(age) < 65: #if at least one person is 15-65 years old,
                        #if return_values(i,'GTGP_area') != 'None' and return_values(i, 'GTGP_area') != '[]':
                        self.GTGP_part = 1  #enroll them
                        break #avoid redundant flagging
                except:
                    pass #covers situations in which age is 'NoneType'
            if self.GTGP_part == 1:
                self.GTGP_coef = random.uniform(0,0.51)  #random coefficient
                self.GTGP_comp = 15  #calculated later
            if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp/self.income) > self.comp_sign:
                if self.num_labor > 0:
                    self.num_labor -= 1
                    self.num_mig += 1  #migration occurs
            if self.num_labor < self.min_req_labor:
                self.GTGP_part_flag = 1  #sets flag for enrollment of more land

        #chance = random.random()
        #if chance > 0.95:
        #    self.GTGP_part_flag = 1

    def step(self):
        """See pseudo-code document"""
        self.gtgp_change()

#class CommunityAgent(Agent):
    #will set attributes later on

class IndividualAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, individual_id, model):
        super().__init__(individual_id, model, age = 20, gender = 1, education = 1)
        self.age = age
        self.gender = gender
        self.education = education

class LandParcelAgent(HouseholdAgent):
    """Sets Individual agents; superclass is HouseholdAgent"""
    def __init__(self, land_id, model, pos, GTGP = 1, area = 1, latitude = 0,
        longitude = 0, plant_type = 1):
        super().__init__(land_id, model)
        self.pos = pos
        self.GTGP = GTGP  #binary (GTGP status of land parcel)
        self.area = area
        self.latitude = latitude
        self.longitude = longitude
        self.plant_type = plant_type

    def step(self):
        """See pseudo-code document"""
        #6/6/2017 start
        self.area = 1

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model, GTGP_comp):
        super().__init__(policy_id, model)
        self.GTGP_comp = 1
        #more attributes will be added later on