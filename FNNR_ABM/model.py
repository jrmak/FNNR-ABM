from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from agents import *
from excel_import import *

class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, n_agents, width, height, GTGP_land = 0, GTGP_latitude = 0, GTGP_longitude = 0,
                 num_mig = 0, mig_prob = 0.5, min_req_labor = 0, num_labor = 0, GTGP_part = 0,
                 GTGP_coef = 0, GTGP_part_flag = 0, area = 1, admin_village = 1):
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
        self.area = area
        self.admin_village = admin_village

        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        #class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        #methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = RandomActivation(self)
        self.make_hh_agents()
        self.make_land_agents()
        self.running = True

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

    #Create agents
    def make_hh_agents(self):
        """Create the household agents"""
        for hh_id in hh_id_list:  # from excel_import
            pos = self.determine_pos(hh_id, 'house_latitude', 'house_longitude')
            try:
                hh = HouseholdAgent(hh_id, self, pos, self.admin_village, self.GTGP_part, self.GTGP_land,
                                self.GTGP_coef, self.mig_prob, self.num_mig, self.min_req_labor,
                                self.num_labor)
                hh.admin_village = 1
                self.space.place_agent(hh, pos) #admin_village placeholder
                self.schedule.add(hh)
            except:
                pass

    def make_land_agents(self):
        """Create the land agents on the map"""
        #add non-GTGP land parcels
        for hh_id in hh_id_list: #from excel_import
            pos = self.determine_pos(hh_id, 'non_GTGP_latitude', 'non_GTGP_longitude')
            try:
                lp = LandParcelAgent(hh_id, self, pos, self.area, self.GTGP_part_flag)
                lp.GTGP_part_flag = 0
                self.space.place_agent(lp, pos)
                self.schedule.add(lp)
            except:
                pass
        #add GTGP land parcels
        for hh_id in hh_id_list: #from excel_import
            pos = self.determine_pos(hh_id, 'GTGP_latitude', 'GTGP_longitude')
            try:
                lp = LandParcelAgent(hh_id, self, pos, self.area, self.GTGP_part_flag)
                lp.GTGP_part_flag = 1
                self.space.place_agent(lp, pos)
                self.schedule.add(lp)
            except:
                #hh_id_list.remove(hh_id)
                #print(hh_id_list)
                pass

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()