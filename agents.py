from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class HouseholdAgent(Agent): #child class of Mesa's generic Agent class
    """Sets household data and head-of-house info"""
    def __init__(self, hh_id, model):
        super().__init__(hh_id, model)
        self.f_id = 1 #individual attributes: head of household only for now
        self.f_age = 1
        self.f_gender = 1 #binary
        self.f_education = 1
        self.land = 1000
        self.GTGP_land = 1000
        self.non_GTGP_land = 1000
        self.NCFP = 1 #binary
        self.num_mig = 1

        #land-parcel attributes; first only
        self.fl_GTGP = 1
        self.fl_area = 1000
        self.fl_plant_type = 1

        self.GTGP_part = 1 #binary
        self.income = 1
        self.mig_prob = 0.5 #migration probability: will need to calc later, preset 0.5
        self.num_labor = 1
        self.min_req_labor = 1 #preset
        self.comp_sign = 0.1 #preset
        #more attributes will be added later on

    def step(self):
        if 15 < self.f_age < 65:
            if self.GTGP_land != 0:
                self.GTGP_coef = random.random()
                #self.GTGP_comp = calculated
                if (self.GTGP_coef * self.GTGP_part) > self.mig_prob and (self.GTGP_comp/self.income) > self.comp_sign:
                    self.num_labor -= 1
                    self.num_mig += 1 #migration

        if (self.num_labor < self.min_req_labor):
            GTGP_part = 1

#class CommunityAgent(Agent):
    #will set attributes later on

class PESAgent(Agent):
    """Sets PES policy agents"""
    def __init__(self, policy_id, model):
        super().__init__(policy_id, model)
        self.GTGP_comp = 1
        #more attributes will be added later on

class ABM(Model):
    """TBD"""
    def __init__(self, n_agents, width, height):
        self.num_agents = n_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        #Create agents
        for i in range(self.num_agents):
            a = HouseholdAgent(i, self)
            self.schedule.add(a)

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()

