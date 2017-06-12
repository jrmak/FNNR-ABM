# !/usr/bin/python

"""
This document runs the main model, placing agents into the ABM.
"""

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from agents import *
from excel_import import *


def show_num_mig(model):
    """Returns the average # of migrants / year in each household"""
    num_mig = [agent.num_mig for agent in model.schedule.agents]
    X = sorted(num_mig)
    num_agents = model.num_agents
    B = sum(X) / num_agents  # 17: 1999-2016
    #print(B)
    return B

class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, num_agents, width, height, GTGP_land = 0, GTGP_latitude = 0, GTGP_longitude = 0,
                 num_mig = 0, mig_prob = 0.5, min_req_labor = 0, num_labor = 0, GTGP_part = 0,
                 GTGP_coef = 0, GTGP_part_flag = 0, area = 1, admin_village = 1, GTGP_enrolled = 0):
        # default values set for now, will define when model runs agents

        self.num_agents = num_agents
        self.GTGP_land = GTGP_land
        self.GTGP_latitude = GTGP_latitude
        self.GTGP_longitude = GTGP_longitude
        self.num_mig = num_mig
        self.mig_prob = mig_prob
        self.min_req_labor = min_req_labor
        self.num_labor = num_labor
        self.GTGP_part = GTGP_part
        self.GTGP_coef = GTGP_coef
        self.GTGP_part_flag = GTGP_part_flag
        self.area = area
        self.admin_village = admin_village
        self.GTGP_enrolled = 0

        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        # class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        # methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = RandomActivation(self)
        self.make_hh_agents()
        self.make_land_agents()
        self.running = True

        self.datacollector = DataCollector(
            model_reporters={'Average Number of Migrants': show_num_mig},
            agent_reporters={'Migrants': lambda a: a.num_mig})


    def determine_pos(self, hh_id, latitude, longitude):
        """Determine position of agent on map"""
        try:
            x = convert_fraction_lat(
                convert_lat_long(
                    str(return_values(hh_id, latitude))
                )
            ) * self.space.x_max

            y = convert_fraction_long(
                convert_lat_long(
                    str(return_values(hh_id, longitude))
                )
            ) * self.space.y_max
            pos = (x, y)
            return pos
        except:
            pass

    # Create agents
    def make_hh_agents(self):
        """Create the household agents"""
        for hh_id in agents:  # from excel_import
            hhpos = self.determine_pos(hh_id, 'house_latitude', 'house_longitude')
            try:
                global a
                a = HouseholdAgent(hh_id, self, hhpos, self.admin_village, self.GTGP_part, self.GTGP_land,
                                    self.GTGP_coef, self.mig_prob, self.num_mig, self.min_req_labor,
                                    self.num_labor)
                a.admin_village = 1
                self.space.place_agent(a, hhpos)  # admin_village placeholder
                self.schedule.add(a)

            except:
                pass

    def make_land_agents(self):
        """Create the land agents on the map"""
        # add non-GTGP land parcels
        for hh_id in agents:  # from excel_import
            landpos = self.determine_pos(hh_id, 'non_GTGP_latitude', 'non_GTGP_longitude')
            try:
                lp = LandParcelAgent(hh_id, self, landpos, self.area, self.GTGP_enrolled)
                lp.GTGP_enrolled = 0
                self.space.place_agent(lp, landpos)
                self.schedule.add(lp)
            except:
                pass
        # add GTGP land parcels
        for hh_id in agents:  # from excel_import
            landpos = self.determine_pos(hh_id, 'GTGP_latitude', 'GTGP_longitude')
            try:
                lp2 = LandParcelAgent(hh_id, self, landpos, self.area, self.GTGP_enrolled)
                lp2.GTGP_enrolled = 1
                self.space.place_agent(lp2, landpos)
                self.schedule.add(lp2)
            except:
                # agents.remove(hh_id)
                # print(agents)
                pass

    def step(self):
        """Advance the model by one step"""
        self.datacollector.collect(self)
        self.schedule.step()
        #for i in range(10):
        #    self.schedule.step()  # run 10 steps at once
