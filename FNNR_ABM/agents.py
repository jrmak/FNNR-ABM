from mesa import Agent #Agent superclass from mesa
import random
from FNNR_ABM.excel_import import *

class HouseholdAgent(Agent):  #child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, hh_id, model, pos, f_id = 1, f_age = 20, f_gender = 1,
                 f_education = 1, land_area = 100, GTGP_land = 50, non_GTGP_land = 50,
                 GTGP_latitude = 20, GTGP_longitude = 100, non_GTGP_latitude = 20,
                 non_GTGP_longitude = 100, NCFP = 1, num_mig = 1, fl_GTGP = 1,
                 fl_area = 100, fl_plant_type = 1, GTGP_part = 0, income = 100,
                 mig_prob = 0.5, num_labor = 20, min_req_labor = 10, comp_sign = 0.1,
                 GTGP_coef = 0, GTGP_part_flag = 0):

        super().__init__(hh_id, model)
        self.f_id = f_id  #individual attributes: head of household only for now
        #f = first person only
        self.pos = pos
        self.f_age = f_age
        self.f_gender = f_gender
        self.f_education = f_education
        self.land_area = land_area  #total land area
        self.GTGP_land = GTGP_land  #area
        self.non_GTGP_land = non_GTGP_land  #area
        self.GTGP_latitude = GTGP_latitude  #first land parcel only
        self.GTGP_longitude =  GTGP_longitude
        self.non_GTGP_latitude = non_GTGP_latitude
        self.non_GTGP_longitude = non_GTGP_longitude
        self.NCFP = NCFP  #another PES program
        self.num_mig = num_mig  #how many migrants the hh currently has

        #land-parcel attributes; first land parcel (fl) only
        self.fl_GTGP = fl_GTGP  #binary (GTGP status of land parcel)
        self.fl_area = fl_area
        self.fl_plant_type = fl_plant_type

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
        """See pseudo-code document: predicts GTGP participation"""
        for i in hh_id_list:  #for each household,
            try:
                self.f_age = float(return_values(i, 'age'))  #pull age of first person from data
            except:
                pass  #pass over None data
            if 15 < self.f_age < 65:
                if return_values(i,'GTGP_area') != 'None' and return_values(i, 'GTGP_area') != '[]':
                    self.GTGP_part = 1
                else:
                    self.GTGP_part = 0
            if self.GTGP_part == 1:
                self.GTGP_coef = random.uniform(0,0.51) #random coefficient
                self.GTGP_comp = 15 #calculated later
            if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp/self.income) > self.comp_sign:
                if self.num_labor > 0:
                    self.num_labor -= 1
                    self.num_mig += 1 #migration occurs
            if self.num_labor < self.min_req_labor:
                self.GTGP_part_flag = 1 #enrollment of more land

        #chance = random.random()
        #if chance > 0.95:
        #    self.GTGP_part_flag = 1


    def step(self):
        """See pseudo-code document"""
        self.gtgp_change()

#class CommunityAgent(Agent):
    #will set attributes later on

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model):
        super().__init__(policy_id, model)
        self.GTGP_comp = 1
        #more attributes will be added later on