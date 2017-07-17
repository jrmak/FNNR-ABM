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

x = []


def show_num_mig(model):
    """Returns the average # of migrants / year in each household"""
    num_mig = [agent.num_mig for agent in model.schedule.agents]
    num_agents = 94
    b = sum(num_mig) / num_agents
    return b

def show_single_male(model):
    return len(single_male_list)

def show_marriages(model):
    for agent in model.schedule.agents:
        try:
            if agent.marriage_flag == 0 or agent.marriage_flag == 1:
                marriage_flag = agent.marriage_flag
                if marriage_flag == 1:
                    x.append(marriage_flag)
        except:
            marriage_flag = 0
            pass
    b = sum(x)
    return b

formermax = []


class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, hh_id, width, height, hh_row = 0, gtgp_land = 0, gtgp_latitude = 0, gtgp_longitude = 0,
                 num_mig = 0, mig_prob = 0.5, min_req_labor = 0, num_labor = 0, gtgp_part = 0,
                 gtgp_coef = 0, gtgp_part_flag = 0, area = 1, maximum = 0, admin_village = 1,
                 gtgp_enrolled = 0, income = 0, gtgp_comp = 0, age = 21, gender = 1, marriage = 0,
                 education = 1, workstatus = 1, birth_rate = 0.1, marriage_rate = 0.1, death_rate = 0.1,
                 birth_interval = 2, marriage_flag = 0, match_prob = 0.05, immi_marriage_rate = 0.03,
                 mig_flag = 0, past_hh_id = 0, last_birth_time = 0, mig_years = 0):
                 # default values set for now, will define when model runs agents

        super().__init__()
        self.hh_id = hh_id
        self.hh_row = hh_row
        self.gtgp_land = gtgp_land
        self.gtgp_latitude = gtgp_latitude
        self.gtgp_longitude = gtgp_longitude
        self.num_mig = num_mig
        self.mig_prob = mig_prob
        self.min_req_labor = min_req_labor
        self.num_labor = num_labor
        self.gtgp_part = gtgp_part
        self.gtgp_coef = gtgp_coef
        self.gtgp_part_flag = gtgp_part_flag

        self.area = area
        self.admin_village = admin_village
        self.gtgp_enrolled = gtgp_enrolled
        self.maximum = maximum
        self.income = income
        self.gtgp_comp = gtgp_comp

        self.age = age
        self.gender = gender
        self.education = education
        self.workstatus = workstatus
        self.marriage = marriage
        self.birth_rate = birth_rate
        self.birth_interval = birth_interval
        self.death_rate = death_rate
        self.marriage_rate = marriage_rate
        self.marriage_flag = marriage_flag
        self.match_prob = match_prob
        self.immi_marriage_rate = immi_marriage_rate
        self.mig_flag = mig_flag
        self.past_hh_id = past_hh_id
        self.last_birth_time = last_birth_time
        self.mig_years = mig_years

        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        # class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        # methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = StagedActivation(self)
        self.make_hh_agents()
        self.make_land_agents()
        self.make_individual_agents()
        self.running = True

        # DataCollector: part of Mesa library
        self.datacollector = DataCollector(
            model_reporters = {'Average Number of Migrants': show_num_mig}
            )
#            agent_reporters={'Migrants': lambda a: a.num_mig})

        self.datacollector2 = DataCollector(
            model_reporters = {'Total # of Marriages in the Reserve': show_marriages})
#            agent_reporters={'Migrants': lambda a: a.marriage})

    def return_x(self, hh_id, latitude):
        """Returns latitudes of land parcels for a given household"""
        convertedlist = []
        try:
            xlist = convert_fraction_lat(
                    convert_decimal(
                        str(return_values(hh_id, latitude))
                    ))
            if type(xlist) is not None:
                for i in range(len(xlist)):
                    x = xlist[i] * self.space.x_max  # fraction times space
                    convertedlist.append(x)
        except TypeError:
            pass
        return convertedlist

    def return_y(self, hh_id, longitude):
        """Returns longitudes of land parcels for a given household"""
        convertedlist = []
        try:
            ylist = convert_fraction_long(
                convert_decimal(
                    str(return_values(hh_id, longitude))
                ))
            for i in range(len(ylist)):
                y = ylist[i] * self.space.y_max  # fraction times space
                convertedlist.append(y)
        except TypeError:
            pass
        return convertedlist

    def return_lp_pos_list(self, xlist, ylist):
        """Returns a list of tuples containing coordinates of land parcels"""
        convertedlist = []
        for i in range(len(xlist)):
            x = xlist[i]
            y = ylist[i]
            pos = (x, y)
            convertedlist.append(pos)
        return convertedlist

    def determine_hhpos(self, hh_id, latitude, longitude):
        """Determine position of agent on map"""
        x = convert_fraction_lat(
            convert_decimal(
                str(return_values(hh_id, latitude))
                )
            )[0] * self.space.x_max

        y = convert_fraction_long(
            convert_decimal(
                str(return_values(hh_id, longitude))
                )
            )[0] * self.space.y_max
        pos = (x, y)
        return pos

    def determine_landpos(self, hh_id, latitude, longitude):
        """Combines previous functions to return a list of land parcel coordinates"""
        latlist = self.return_x(hh_id, latitude)
        longlist = self.return_y(hh_id, longitude)
        return self.return_lp_pos_list(latlist, longlist)

    def calc_distance(self, landpos, hhpos):
        """Given a household id, return the distances between household and parcels"""
        if landpos is not None and hhpos is not None:
            distance = sqrt(
                (landpos[0] - hhpos[0]) ** 2 + (landpos[1] - hhpos[1]) ** 2
                )
            if distance < 10:
                return distance

    # Create agents
    def make_hh_agents(self):
        """Create the household agents"""
        for hh_row in agents:  # agents is a list of ints 1-97 from excel_import
            hhpos = self.determine_hhpos(hh_row, 'house_latitude', 'house_longitude')
            hh_id = return_values(hh_row, 'hh_id')
            self.hh_id = hh_id
            a = HouseholdAgent(hh_row, self, hhpos, self.hh_id, self.admin_village, self.gtgp_part, self.gtgp_land,
                               self.gtgp_coef, self.mig_prob, self.num_mig, self.min_req_labor,
                               self.num_labor, self.income, self.gtgp_comp)
            a.admin_village = 1  # see server.py, line 22
            self.space.place_agent(a, hhpos)  # admin_village placeholder
            self.schedule.add(a)

    def make_land_agents(self):
        """Create the land agents on the map"""
        # add non-gtgp land parcels
        for hh_row in agents:  # from excel_import
            hhpos = self.determine_hhpos(hh_row, 'house_latitude', 'house_longitude')
            maxlist = []
            landposlist = self.determine_landpos(hh_row, 'non_gtgp_latitude', 'non_gtgp_longitude')
            hh_id = return_values(hh_row, 'hh_id')
            for landpos in landposlist:
                distance = self.calc_distance(hhpos, landpos)
                if distance not in formermax:
                    maxlist.append(distance)
                    formermax.append(distance)
                lp = LandParcelAgent(hh_id, self, landpos, hh_row, self.maximum, self.area, self.gtgp_enrolled)
                if maxlist != ['']:
                    try:
                        max_index = maxlist.index(max(maxlist))
                        if landpos == landposlist[max_index]:
                            lp.maximum = 1
                        else:
                            lp.maximum = 0
                    except:
                        pass
                else:
                    lp.maximum = 0
                lp.gtgp_enrolled = 0
                self.space.place_agent(lp, landpos)
                self.schedule.add(lp)

        # add gtgp land parcels
        for hh_row in agents:  # from excel_import
            hh_id = return_values(hh_row, 'hh_id')
            landposlist = self.determine_landpos(hh_row, 'gtgp_latitude', 'gtgp_longitude')
            for landpos in landposlist:
                lp2 = LandParcelAgent(hh_id, self, landpos, hh_row, self.area, self.gtgp_enrolled)
                lp2.gtgp_enrolled = 1
                self.space.place_agent(lp2, landpos)
                self.schedule.add(lp2)

    def make_individual_agents(self):
        """Create the individual agents"""
        for hh_row in agents:  # agents is a list of ints 1-96 from excel_import
            individual_id_list = return_values(hh_row, 'name')
            hh_id = return_values(hh_row, 'hh_id')
            self.hh_id = hh_id
            agelist = return_values(hh_row, 'age')  # find the ages of people in hh
            genderlist = return_values(hh_row, 'gender')
            marriagelist = return_values(hh_row, 'marriage')
            if individual_id_list is not None and individual_id_list is not []:
                for i in range(len(individual_id_list)):
                    self.individual_id = str(self.hh_id) + str(individual_id_list[i])  # example: 2c
                    # if agelist is not None and agelist is not []:
                    self.age = agelist[i]
                    # if genderlist is not None and genderlist is not []:
                    self.gender = genderlist[i]
                    self.marriage = marriagelist[i]
                    if 15 < self.age < 59:
                        self.workstatus == 1
                    else:
                        self.workstatus == 0
                    ind = IndividualAgent(hh_row, self, self.hh_id, self.individual_id, self.age, self.gender,
                                          self.education, self.workstatus, self.marriage, self.birth_rate,
                                          self.birth_interval, self.death_rate, self.marriage_rate, self.marriage_flag,
                                          self.mig_flag, self.match_prob, self.immi_marriage_rate, self.past_hh_id,
                                          self.last_birth_time, self.mig_years)
                    # hh_id twice as placeholder test at home
                    self.schedule.add(ind)

    def step(self):
        """Advance the model by one step"""
        self.datacollector.collect(self)
        self.datacollector2.collect(self)
        self.schedule.step()
