from mesa import Agent, Model
import random

class HouseholdAgent(Agent): #child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    #dummy code for now; will import data later to be used
    def __init__(self, hh_id, model, f_id = 1, f_age = 20, f_gender = 1,
                 f_education = 1, land = 100, GTGP_land = 50, non_GTGP_land = 50,
                 GTGP_latitude = 20, GTGP_longitude = 100, non_GTGP_latitude = 20,
                 non_GTGP_longitude = 100, NCFP = 1, num_mig = 1, fl_GTGP = 1,
                 fl_area = 100, fl_plant_type = 1, GTGP_part = 1, income = 100,
                 mig_prob = 0.5, num_labor = 1, min_req_labor = 1, comp_sign = 0.1):

        super().__init__(hh_id, model)
        self.f_id = f_id #individual attributes: head of household only for now
        self.f_age = f_age
        self.f_gender = f_gender #binary
        self.f_education = f_education
        self.land = land
        self.GTGP_land = GTGP_land
        self.non_GTGP_land = non_GTGP_land
        self.GTGP_latitude = GTGP_latitude
        self.GTGP_longitude =  GTGP_longitude
        self.non_GTGP_latitude = non_GTGP_latitude
        self.non_GTGP_longitude = non_GTGP_longitude
        self.NCFP = NCFP
        self.num_mig = num_mig

        #land-parcel attributes; first only
        self.fl_GTGP = fl_GTGP
        self.fl_area = fl_area
        self.fl_plant_type = fl_plant_type

        self.GTGP_part = GTGP_part #binary
        self.income = income
        self.mig_prob = mig_prob #migration probability: will need to calc later, preset 0.5
        self.num_labor = num_labor
        self.min_req_labor = min_req_labor #preset
        self.comp_sign = comp_sign #preset
        #more attributes will be added later on

    def step(self):
        """See pseudo-code document"""
        if 15 < self.f_age < 65:
            if self.GTGP_land != 0:
                self.GTGP_coef = random.random()
                #self.GTGP_comp = calculated later
                if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp/self.income) > self.comp_sign:
                    self.num_labor -= 1
                    self.num_mig += 1 #migration

        if self.num_labor < self.min_req_labor:
            self.GTGP_part = 1

#class CommunityAgent(Agent):
    #will set attributes later on

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model):
        super().__init__(policy_id, model)
        self.GTGP_comp = 1
        #more attributes will be added later on