from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from FNNR_ABM.agents import HouseholdAgent
from FNNR_ABM.excel_import import *

class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, n_agents, width, height, GTGP_land = 0, GTGP_latitude = 0, GTGP_longitude = 0,
                 num_mig = 0, mig_prob = 0.5, min_req_labor = 0, num_labor = 0, GTGP_part = 0,
                 GTGP_coef = 0, GTGP_part_flag = 0):
        #default values set for now, will define when model runs agents
        self.num_agents = n_agents
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
        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        #class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        #methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = RandomActivation(self)
        self.make_agents()
        self.running = True

    #Create agents
    def make_agents(self):
        """Create the household agents"""
        #first land parcel only for now
        for i in hh_id_list: #from excel_import
            try:
                x = convert_fraction_lat(
                    convert_lat_long(
                        str(return_values(i, 'GTGP_latitude'))
                    )
                ) * self.space.x_max

                y = convert_fraction_long(
                    convert_lat_long(
                        str(return_values(i, 'GTGP_longitude'))
                    )
                ) * self.space.y_max
            except:
                pass
            pos = (x,y)
            try:
                f_age = float(return_values(i, 'age'))
            except:
                pass
                #ignores if household has no land parcels
            hh = HouseholdAgent(i, self, pos, self.GTGP_part, f_age, self.GTGP_land,
                            self.GTGP_coef, self.mig_prob, self.num_mig, self.min_req_labor,
                            self.num_labor)
            try:
                self.space.place_agent(hh, pos)
            except:
                pass
            self.schedule.add(hh)

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()