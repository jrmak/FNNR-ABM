# !/usr/bin/python

"""
This document runs the main model, placing agents into the ABM.
"""

from mesa import Model
from mesa.time import StagedActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from agents import *
from excel_import import *
from math import sqrt

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
                 GTGP_coef = 0, GTGP_part_flag = 0, area = 1, maximum = 0, admin_village = 1, GTGP_enrolled = 0):
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
        self.GTGP_enrolled = GTGP_enrolled
        self.maximum = maximum

        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        # class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        # methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = StagedActivation(self)
        self.make_hh_agents()
        self.make_land_agents()
        self.running = True

        self.datacollector = DataCollector(
            model_reporters={'Average Number of Migrants': show_num_mig},
            agent_reporters={'Migrants': lambda a: a.num_mig})


    def return_x(self, hh_id, latitude):
        """Returns latitudes of land parcels for a given household"""
        convertedlist = []
        try:
            xlist = convert_fraction_lat(
                    convert_lat_long(
                        str(return_values(hh_id, latitude))
                    ))
            teststr = str(return_values(hh_id, latitude))
            # print(convert_lat_long(teststr),'!')
            # print(xlist)
            if type(xlist) is not None:
                for i in range(len(xlist)):
                    x = xlist[i] * self.space.x_max
                    convertedlist.append(x)
        except TypeError:
            pass
        # print(convertedlist)
        return convertedlist

    def return_y(self, hh_id, longitude):
        """Returns longitudes of land parcels for a given household"""
        # print(convert_lat_long(
        #            str(return_values(hh_id, longitude))
        #        ))
        convertedlist = []
        try:
            ylist = convert_fraction_long(
                convert_lat_long(
                    str(return_values(hh_id, longitude))
                ))
            #print(ylist)
            for i in range(len(ylist)):
                y = ylist[i] * self.space.y_max
                convertedlist.append(y)
        except TypeError:
            pass
        return convertedlist

    def return_lp_pos_list(self, xlist, ylist):
        """Returns a list of tuples containing coordinates of land parcels"""
        convertedlist = []
        # print(xlist)
        # print(ylist)
        for i in range(len(xlist)):
            x = xlist[i]
            y = ylist[i]
            pos = (x, y)
            convertedlist.append(pos)
        return convertedlist

    def determine_hhpos(self, hh_id, latitude, longitude):
        """Determine position of agent on map"""
        try:
            x = convert_fraction_lat(
                convert_lat_long(
                    str(return_values(hh_id, latitude))
                )
            )[0] * self.space.x_max

            y = convert_fraction_long(
                convert_lat_long(
                    str(return_values(hh_id, longitude))
                )
            )[0] * self.space.y_max
            pos = (x, y)
            return pos
        except TypeError:
            pass

    def determine_landpos(self, hh_id, latitude, longitude):
        """Combines previous functions to return a list of land parcel coordinates"""
        latlist = self.return_x(hh_id, latitude)
        longlist = self.return_y(hh_id, longitude)
        return self.return_lp_pos_list(latlist, longlist)

    def calc_distance(self, landpos, hhpos):
        """Given a household id, return the distances between household and parcels"""
        # 6/14/2017 currently working on
        distance = sqrt(
            (landpos[0] - hhpos[0]) ** 2 + (landpos[1] - hhpos[1]) ** 2
            )
        if distance < 10:
            return distance

    # Create agents
    def make_hh_agents(self):
        """Create the household agents"""
        for hh_id in agents:  # agents is a list of ints 1-97 from excel_import
            hhpos = self.determine_hhpos(hh_id, 'house_latitude', 'house_longitude')
            try:
                global a
                a = HouseholdAgent(hh_id, self, hhpos, self.admin_village, self.GTGP_part, self.GTGP_land,
                                    self.GTGP_coef, self.mig_prob, self.num_mig, self.min_req_labor,
                                    self.num_labor)
                a.admin_village = 1
                self.space.place_agent(a, hhpos)  # admin_village placeholder
                self.schedule.add(a)

            except TypeError:
                pass

    def make_land_agents(self):
        """Create the land agents on the map"""
        # add non-GTGP land parcels
        for hh_id in agents:  # from excel_import
            hhpos = self.determine_hhpos(hh_id, 'house_latitude', 'house_longitude')
            maxlist = []
            landposlist = self.determine_landpos(hh_id, 'non_GTGP_latitude', 'non_GTGP_longitude')
            # print(landposlist) #list should have multiple tuples
            for landpos in landposlist:
                distance = self.calc_distance(hhpos, landpos)
                maxlist.append(distance)
            # print(hh_id, maxlist)
#            try:
#                if maxlist != ['']:
#                    max_index = maxlist.index(max(maxlist))
#                    #print(max_index, 'index')
#            except:
#                pass
            for landpos in landposlist:
                lp = LandParcelAgent(hh_id, self, landpos, self.maximum, self.area, self.GTGP_enrolled)
                if maxlist != [''] and maxlist[0] != None:
                    try:
                        max_index = maxlist.index(max(maxlist))
                        if landpos == landposlist[max_index]:
                            lp.maximum = 1
                            # print(lp.maximum, 'lp.maximum')
                        else:
                            lp.maximum = 0
                            #print(lp.maximum, 'else1')
                    except:
                        pass
                else:
                    lp.maximum = 0
                    #print(lp.maximum, 'else2')
                lp.GTGP_enrolled = 0
                self.space.place_agent(lp, landpos)
                self.schedule.add(lp)

        # add GTGP land parcels
        for hh_id in agents:  # from excel_import
            hhpos = self.determine_hhpos(hh_id, 'house_latitude', 'house_longitude')
            maxlist = []
            landposlist = self.determine_landpos(hh_id, 'GTGP_latitude', 'GTGP_longitude')
            for landpos in landposlist:
                lp2 = LandParcelAgent(hh_id, self, landpos, self.area, self.GTGP_enrolled)
                lp2.GTGP_enrolled = 1
                self.space.place_agent(lp2, landpos)
                self.schedule.add(lp2)
    def step(self):
        """Advance the model by one step"""
        self.datacollector.collect(self)
        self.schedule.step()
        #for i in range(10):
        #    self.schedule.step()  # run 10 steps at once
