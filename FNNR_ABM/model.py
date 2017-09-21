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
from random import choice


hh_list_2014 = ['11', '16', '31', '39', '41', '57', '72', '91', '101', '104', '108',
                '109', '113', '120', '123', '148', '149', '153', '161', '166']


def show_cumulative_mig(model):
    """Returns the cumulative # of out-migrants from the reserve at any given time"""
    return sum(cumulative_mig_list)


def show_instant_mig(model):
    """Returns the 'instant' # of out-migrants from the reserve at any given time"""
    return len(out_migrants_list)


def show_instant_mig_per_hh(model):
    """Returns the average # of migrants from each household at a given time"""
    return len(out_migrants_list) / 94


def show_cumulative_re_mig(model):
    """Returns the cumulative # of re-migrants"""
    return sum(cumulative_re_mig_list)


def show_instant_re_mig(model):
    """Returns the 'instant' # of out-migrants from the reserve at any given time"""
    return len(re_migrants_list)


def show_instant_re_mig_per_hh(model):
    """Returns the average # of re-migrants for each household"""
    return len(re_migrants_list) / 94


def show_marriages(model):
    """Returns the total # of marriages in the reserve"""
    return float(len(new_married_list))


def show_births(model):
    """Returns the total # of births in the reserve"""
    return len(birth_list)


def show_deaths(model):
    """Returns the total # of deaths in the reserve"""
    return len(death_list)


def show_hh_size(model):
    """Returns the average household size in the reserve"""
    return sum(hh_size_list) / 94


def show_num_labor(model):
    """Returns the average # of laborers per household in the reserve"""
    return sum(num_labor_list) / 94


def show_income(model):
    """Returns the average household income in the reserve"""
    return sum(household_income_list) / 94


def show_pop(model):
    """Returns the population for each year in the reserve"""
    individuals = 278 + len(birth_list) - len(out_migrants_list) - len(death_list)
    # 278 = original individual count, excluding initial migrants
    # out_migrants_list at step 0 includes initial migrants
    return individuals


def show_gtgp_per_hh(model):
    """Returns the average # of GTGP land parcels per household"""
    return len(gtgplist) / 94


def show_non_gtgp_per_hh(model):
    """Returns the average # of non-GTGP land parcels per household"""
    return len(nongtgplist) / 94


# 2014


def show_cumulative_mig_2014(model):
    """Returns the cumulative # of migrants"""
    return sum(cumulative_mig_list_2014)


def show_instant_mig_2014(model):
    """Returns the 'instant' # of out-migrants from the reserve at any given time"""
    return len(out_migrants_list_2014)


def show_instant_mig_per_hh_2014(model):
    """Returns the average # of migrants from each household at a given time"""
    return len(out_migrants_list_2014) / 20


def show_cumulative_re_mig_2014(model):
    """Returns the cumulative # of re-migrants"""
    return sum(cumulative_re_mig_list_2014)


def show_instant_re_mig_2014(model):
    """Returns the instant # of re-migrants"""
    return len(re_migrants_list_2014)


def show_instant_re_mig_per_hh_2014(model):
    """Returns the average cumulative # of re-migrants for each household"""
    return len(re_migrants_list_2014) / 20


def show_marriages_2014(model):
    """Returns the total # of marriages in the reserve"""
    return float(len(new_married_list_2014))


def show_births_2014(model):
    """Returns the total # of births in the reserve"""
    return len(birth_list_2014)


def show_deaths_2014(model):
    """Returns the total # of deaths in the reserve"""
    return len(death_list_2014)


def show_hh_size_2014(model):
    """Returns the average household size in the reserve"""
    return sum(hh_size_list_2014) / 20


def show_num_labor_2014(model):
    """Returns the average # of laborers per household in the reserve"""
    return sum(num_labor_list_2014) / 20


def show_income_2014(model):
    """Returns the average household income in the reserve"""
    return sum(household_income_list_2014) / 20


def show_pop_2014(model):
    """Returns the population for each year in the reserve"""
    individuals = 59 + len(birth_list_2014) - len(out_migrants_list_2014) - len(death_list_2014)
    # 59 = original individual count, excluding initial migrants
    # out_migrants_list at step 0 includes initial migrants
    return individuals


def show_gtgp_per_hh_2014(model):
    """Returns the average # of GTGP land parcels per household"""
    return len(gtgplist_2014) / 20


def show_non_gtgp_per_hh_2014(model):
    """Returns the average # of non-GTGP land parcels per household"""
    return len(nongtgplist_2014) / 20


class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, hh_id, width, height):
        # default values set for now, will define when model runs agents

        super().__init__()
        self.hh_id = hh_id
        self.hh_row = 0
        self.gtgp_land = 0
        self.gtgp_latitude = 0
        self.gtgp_longitude = 0
        self.num_mig = 0
        self.mig_prob = 0
        self.min_req_labor = 0
        self.num_labor = 0
        self.gtgp_coef = 0
        self.gtgp_part_flag = 0
        self.income_local_off_farm = 0

        self.area = 0
        self.admin_village = 0
        self.gtgp_enrolled = 0
        self.income = 0
        self.gtgp_comp = 0
        self.gtgp_net_income = 0

        self.age = 0
        self.age_at_step_0 = 0
        self.gender = 1
        self.education = 0
        self.workstatus = 0
        self.marriage = 0
        self.birth_rate = 0.1
        self.birth_interval = 2
        self.death_rate = 0.1
        self.marriage_rate = 0.1
        self.marriage_flag = 0
        self.match_prob = 0.05
        self.immi_marriage_rate = 0.03
        self.mig_flag = 0
        self.past_hh_id = 0
        self.last_birth_time = 0
        self.mig_years = 0

        self.age_1 = 0
        self.gender_1 = 0
        self.education_1 = 0
        self.land_type = 0
        self.land_time = 0
        self.plant_type = 0
        self.land_area = 0
        self.land_income = 0

        self.total_rice = 0
        self.total_dry = 0
        self.gtgp_rice = 0
        self.gtgp_dry = 0
        self.pre_gtgp_output = 0
        self.non_gtgp_output = 0
        self.hh_size = 0
        self.non_gtgp_area = 0
        self.step_counter = 0

        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        self.schedule = StagedActivation(self)

        self.make_hh_agents_2016()
        self.make_hh_agents_2014()

        self.make_land_agents_2016()
        self.make_land_agents_2014()

        self.make_individual_agents_2016()
        self.make_individual_agents_2014()

        self.running = True

        # DataCollector: part of Mesa library

        self.datacollector = DataCollector(
            model_reporters = {'Cumulative # of Out-Migrants': show_cumulative_mig})

        self.datacollector2 = DataCollector(
            model_reporters = {'Instant # of Out-Migrants (includes multiple counts)': show_instant_mig}
            )

        self.datacollector3 = DataCollector(
            model_reporters={'Cumulative # of Re-migrants (includes multiple counts)': show_cumulative_re_mig})

        self.datacollector4 = DataCollector(
            model_reporters={'Instant # of Re-migrants': show_instant_re_mig})

        self.datacollector5 = DataCollector(
            model_reporters = {'Total # of Marriages in the Reserve': show_marriages})

        self.datacollector6 = DataCollector(
            model_reporters = {'Total # of Births in the Reserve': show_births})

        self.datacollector7 = DataCollector(
            model_reporters = {'Total # of Deaths in the Reserve': show_deaths})

        self.datacollector8 = DataCollector(
            model_reporters = {'Population in the Reserve': show_pop})

        self.datacollector9 = DataCollector(
            model_reporters = {'Average GTGP Parcels Per Household': show_gtgp_per_hh})

        self.datacollector10 = DataCollector(
            model_reporters = {'Average Non-GTGP Parcels Per Household': show_non_gtgp_per_hh})

        self.datacollector11 = DataCollector(
            model_reporters = {'Average Household Size': show_hh_size})

        self.datacollector12 = DataCollector(
            model_reporters = {'# of Laborers Per Household': show_num_labor})

        self.datacollector13 = DataCollector(
            model_reporters = {'Average Household Income': show_income})

        # 2014

        self.datacollector14 = DataCollector(
            model_reporters = {'Cumulative # of Migrants (includes multiple counts)': show_cumulative_mig_2014}
            )

        self.datacollector15 = DataCollector(
            model_reporters = {'Instant # of Migrants': show_instant_mig_2014}
            )

        self.datacollector16 = DataCollector(
            model_reporters={'Cumulative # of Re-migrants (includes multiple counts)': show_cumulative_re_mig_2014})

        self.datacollector17 = DataCollector(
            model_reporters={'Instant # of Re-migrants': show_instant_re_mig_2014})

        self.datacollector18 = DataCollector(
            model_reporters = {'Total # of Marriages in the Reserve': show_marriages_2014})

        self.datacollector19 = DataCollector(
            model_reporters = {'Total # of Births in the Reserve': show_births_2014})

        self.datacollector20 = DataCollector(
            model_reporters = {'Total # of Deaths in the Reserve': show_deaths_2014})

        self.datacollector21 = DataCollector(
            model_reporters = {'Population in the Reserve': show_pop_2014})

        self.datacollector22 = DataCollector(
            model_reporters = {'Average GTGP Parcels Per Household': show_gtgp_per_hh_2014})

        self.datacollector23 = DataCollector(
            model_reporters = {'Average Non-GTGP Parcels Per Household': show_non_gtgp_per_hh_2014})

        self.datacollector24 = DataCollector(
            model_reporters = {'Average Household Size': show_hh_size_2014})

        self.datacollector25 = DataCollector(
            model_reporters = {'# of Laborers Per Household': show_num_labor_2014})

        self.datacollector26 = DataCollector(
            model_reporters = {'Average Household Income': show_income_2014})

    def make_birth_agents(self, ind):
        self.schedule = StagedActivation(self)
        self.schedule.add(ind)
        self.running = True

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

    def determine_hhpos(self, hh_row, latitude, longitude):
        """Determine position of agent on map"""
        x = convert_fraction_lat(
            convert_decimal(
                str(return_values(hh_row, latitude))
                )
            )[0] * self.space.x_max

        y = convert_fraction_long(
            convert_decimal(
                str(return_values(hh_row, longitude))
                )
            )[0] * self.space.y_max
        pos = (x, y)
        return pos

    def determine_landpos(self, hh_row, latitude, longitude):
        """Combines previous functions to return a list of land parcel coordinates"""
        latlist = self.return_x(hh_row, latitude)
        longlist = self.return_y(hh_row, longitude)
        return self.return_lp_pos_list(latlist, longlist)

    # Create agents
    def make_hh_agents_2016(self):
        """Create the household agents for 2016"""
        for hh_row in agents:  # agents is a list of ints 1-97 from excel_import
            self.hhpos = self.determine_hhpos(hh_row, 'house_latitude', 'house_longitude')
            self.hh_id = return_values(hh_row, 'hh_id')
            self.admin_village = 1

            # 2016
            mig_remittances = return_values(hh_row, 'mig_remittances')  # remittances of initial migrant
            if mig_remittances is None:
                mig_remittances = 0
            household_income_list[hh_row - 1] = int(mig_remittances)
            household_remittances_list[hh_row - 1] = int(mig_remittances)

            if return_values(hh_row, 'initial_migrants') is not None:
                out_mig_list[hh_row - 1] = 1
                cumulative_mig_list[hh_row - 1] = 1

            else:
                out_mig_list[hh_row - 1] = 0
                cumulative_mig_list[hh_row - 1] = 0
            num_labor_list[hh_row - 1] = initialize_labor(hh_row)
            hh_size_list[hh_row - 1] = len(return_values(hh_row, 'age'))

            a = HouseholdAgent(hh_row, self, self.hh_id, self.admin_village)
            self.space.place_agent(a, self.hhpos)  # admin_village placeholder
            self.schedule.add(a)

    def make_hh_agents_2014(self):
        """Create the household agents for 2014"""
        hardcoded_remittances = [(2, 3000), (3, 10000), (4, 5000), (7, 2000), (16, 2000),
                                 (17, 36000), (19, 5000), (20, 2000)]
        for (x, y) in hardcoded_remittances:
            household_income_list_2014[x - 2] = y
            household_remittances_list_2014[x - 2] = y

        for hh_row in range(2, 22):  # agents is a list of ints 1-97 from excel_import
            self.hh_id = return_values(hh_row, 'hh_id')
            self.admin_village = 1

            # 2014
            if return_values_2014(hh_row, 'initial_migrants') is not None:
                out_mig_list_2014[hh_row - 2] = 1
                cumulative_mig_list_2014[hh_row - 2] = 1
            else:
                out_mig_list_2014[hh_row - 2] = 0
                cumulative_mig_list_2014[hh_row - 2] = 0

            num_labor_list_2014[hh_row - 2] = initialize_labor_2014(hh_row)
            hh_size_list_2014[hh_row - 2] = len(return_values_2014(hh_row, 'age'))

            a2014 = HouseholdAgent(hh_row, self, self.hh_id, self.admin_village)
            self.schedule.add(a2014)

    def make_land_agents_2016(self):
        """Create the land agents on the map; adding output and time later"""
        # add non-gtgp
        for hh_row in agents:  # from excel_import
            hh_id = return_values(hh_row, 'hh_id')
            self.total_rice = return_values(hh_row, 'non_gtgp_rice_mu')
            if self.total_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.total_dry = return_values(hh_row, 'non_gtgp_dry_mu')
            if self.total_dry in ['-3', '-4', -3, None]:
                self.total_dry = 0
            self.gtgp_rice = return_values(hh_row, 'gtgp_rice_mu')
            if self.gtgp_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.gtgp_dry = return_values(hh_row, 'gtgp_dry_mu')
            if self.gtgp_dry in ['-3', '-4', -3, None]:
                self.gtgp_dry = 0

            landposlist = self.determine_landpos(hh_row, 'non_gtgp_latitude', 'non_gtgp_longitude')
            self.age_1 = return_values(hh_row, 'age')[0]
            self.gender_1 = return_values(hh_row, 'gender')[0]
            self.education_1 = return_values(hh_row, 'education')[0]

            for landpos in landposlist:
                try:
                    self.pre_gtgp_output = return_values(hh_row, 'pre_gtgp_output')[landposlist.index(landpos)]
                except:
                    pass

                try:
                    self.non_gtgp_output = return_values(hh_row, 'pre_gtgp_output')[landposlist.index(landpos)]
                except:
                    pass
                self.land_time = return_values(hh_row, 'non_gtgp_travel_time')[landposlist.index(landpos)]
                try:
                    self.plant_type = return_values(hh_row, 'non_gtgp_plant_type')[landposlist.index(landpos)]
                except:
                    pass
                try:
                    self.land_type = return_values(hh_row, 'non_gtgp_land_type')[landposlist.index(landpos)]
                except:
                    pass
                self.hh_size = len(return_values(hh_row, 'age'))
                self.gtgp_enrolled = 0
                if self.gtgp_enrolled == 0 and self not in nongtgplist and self not in gtgplist:
                    nongtgplist.append(self)
                lp = LandParcelAgent(hh_row, self, hh_id, hh_row, landpos, self.gtgp_enrolled,
                                     self.age_1, self.gender_1, self.education_1,
                                     self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice,
                                     self.land_type, self.land_time, self.plant_type, self.non_gtgp_output,
                                     self.pre_gtgp_output)
                self.space.place_agent(lp, landpos)
                self.schedule.add(lp)
                # except:
                #    pass

        # add gtgp
        for hh_row in agents:  # from excel_import
            hh_id = return_values(hh_row, 'hh_id')
            self.total_rice = return_values(hh_row, 'non_gtgp_rice_mu')
            if self.total_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.total_dry = return_values(hh_row, 'non_gtgp_dry_mu')
            if self.total_dry in ['-3', '-4', -3, None]:
                self.total_dry = 0
            self.gtgp_rice = return_values(hh_row, 'gtgp_rice_mu')
            if self.gtgp_rice in ['-3', '-4', -3, None]:
                self.total_rice = 0
            self.gtgp_dry = return_values(hh_row, 'gtgp_dry_mu')
            if self.gtgp_dry in ['-3', '-4', -3, None]:
                self.gtgp_dry = 0
            landposlist = self.determine_landpos(hh_row, 'gtgp_latitude', 'gtgp_longitude')
            self.age_1 = return_values(hh_row, 'age')[0]
            self.gender_1 = return_values(hh_row, 'gender')[0]
            self.education_1 = return_values(hh_row, 'education')[0]
            for landpos in landposlist:
                try:
                    self.pre_gtgp_output = return_values(hh_row, 'pre_gtgp_output')[landposlist.index(landpos)]
                except:
                    pass
                try:
                    self.non_gtgp_output = return_values(hh_row, 'pre_gtgp_output')[landposlist.index(landpos)]
                except:
                    pass
                try:
                    self.land_time = return_values(hh_row, 'gtgp_travel_time')[landposlist.index(landpos)]
                except:
                    pass
                try:
                    self.plant_type = return_values(hh_row, 'pre_gtgp_plant_type')[landposlist.index(landpos)]
                except:
                    pass
                try:
                    self.land_type = return_values(hh_row, 'pre_gtgp_land_type')[landposlist.index(landpos)]
                except:
                    pass
                self.hh_size = len(return_values(hh_row, 'age'))
                self.gtgp_enrolled = 1
                if self.gtgp_enrolled == 1 and self not in gtgplist:
                    gtgplist.append(self)
                lp_gtgp = LandParcelAgent(hh_id, self, hh_id, hh_row, landpos, self.gtgp_enrolled,
                                        self.age_1, self.gender_1, self.education_1,
                                        self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice,
                                        self.land_type, self.land_time, self.plant_type, self.non_gtgp_output,
                                        self.pre_gtgp_output)
                self.space.place_agent(lp_gtgp, landpos)
                self.schedule.add(lp_gtgp)

    def make_individual_agents_2016(self):
        """Create the individual agents"""
        for hh_row in agents:  # agents is a list of ints 1-94 from excel_import
            individual_id_list = return_values(hh_row, 'name')
            hh_id = return_values(hh_row, 'hh_id')
            self.hh_id = hh_id
            agelist = return_values(hh_row, 'age')  # find the ages of people in hh
            genderlist = return_values(hh_row, 'gender')
            marriagelist = return_values(hh_row, 'marriage')
            educationlist = return_values(hh_row, 'education')
            income_local_off_farm = float(return_values(hh_row, 'income_local_off_farm'))
            income_local_off_farm_list[hh_row - 1] = income_local_off_farm
            household_income_list[hh_row - 1] = household_income_list[hh_row - 1] + income_local_off_farm
            if individual_id_list is not None and individual_id_list is not []:
                for i in range(len(individual_id_list)):
                    self.individual_id = str(self.hh_id) + str(individual_id_list[i])  # example: 2c
                    self.age = int(agelist[i])
                    # if genderlist is not None and genderlist is not []:
                    self.gender = int(genderlist[i])
                    try:
                        self.education = educationlist[i]
                    except:
                        self.education = 0
                    self.marriage = marriagelist[i]
                    IndividualAgent.create_initial_migrant_list(self, hh_row)
                    self.age_at_step_0 = self.age
                    self.income_local_off_farm = return_values(self.hh_row, 'income_local_off_farm')
                    ind = IndividualAgent(hh_row, self, self.hh_id, self.individual_id, self.age, self.gender,
                                          self.education, self.marriage, self.past_hh_id, self.non_gtgp_area,
                                          self.step_counter, self.age_at_step_0, self.income_local_off_farm)
                    self.schedule.add(ind)

    def make_individual_agents_2014(self):
        for hh_id in hh_list_2014:
            self.hh_id = hh_id
            self.hh_row = get_hh_row_2014(int(self.hh_id))
            individual_id_list = return_values_2014(self.hh_row, 'name')
            agelist = return_values_2014(self.hh_row, 'age')  # find the ages of people in hh
            genderlist = return_values_2014(self.hh_row, 'gender')
            marriagelist = return_values_2014(self.hh_row, 'marriage')
            educationlist = return_values_2014(self.hh_row, 'education')

            if self.hh_id == '31':
                income_local_off_farm = (float(7500))
            elif self.hh_id == '39':
                income_local_off_farm = (float(12000))
            elif self.hh_id == '57':
                income_local_off_farm = (float(18000))
            elif self.hh_id == '148':
                income_local_off_farm = (float(9600))
            elif self.hh_id == '153':
                income_local_off_farm = (float(600))
            else:
                income_local_off_farm = 0
            household_income_list_2014[self.hh_row - 2] = household_income_list_2014[self.hh_row - 2] + income_local_off_farm
            income_local_off_farm_list_2014[self.hh_row - 2] = income_local_off_farm
            if individual_id_list is not None and individual_id_list is not []:
                try:
                    self.non_gtgp_area = sum(return_values_2014(self.hh_row, 'non_gtgp_area'))
                except:
                    pass
                for i in range(len(individual_id_list)):
                    self.individual_id = str(self.hh_id) + str(individual_id_list[i]) + '_' + '2014'  # example: 2c
                    self.age = agelist[i]
                    try:
                        self.gender = genderlist[i]
                    except:
                        self.gender = choice([1,2])
                    try:
                        self.education = educationlist[i]
                    except:
                        self.education = 0
                    try:
                        self.marriage = marriagelist[i]
                    except IndexError:
                        self.marriage = 6
                    IndividualAgent.create_initial_migrant_list(self, self.hh_row)
                    self.age_at_step_0 = self.age
                    self.income_local_off_farm = self.income_local_off_farm = return_values_2014(self.hh_row, 'income_local_off_farm')

                    ind = IndividualAgent(hh_id, self, self.hh_id, self.individual_id, self.age,
                                          self.gender, self.education, self.marriage,
                                          self.past_hh_id, self.non_gtgp_area, self.step_counter,
                                          self.age_at_step_0,
                                          self.income_local_off_farm)
                    self.schedule.add(ind)

    def make_land_agents_2014(self):
        """Create the land agents on the map; adding output and time later"""

        agents2014 = range(2, 22)
        # add non-gtgp
        for hh_row in agents2014:  # from excel_import

            try:
                for i in range(len(return_values_2014(hh_row, 'non_gtgp_output'))):
                    self.hh_id = return_values_2014(hh_row, 'hh_id')
                    self.total_rice = return_values_2014(hh_row, 'non_gtgp_rice_mu')
                    if self.total_rice in ['-3', '-4', -3, None]:
                        self.total_rice = 0
                    self.total_dry = return_values_2014(hh_row, 'non_gtgp_dry_mu')
                    if self.total_dry in ['-3', '-4', -3, None]:
                        self.total_dry = 0
                    self.gtgp_rice = return_values_2014(hh_row, 'gtgp_rice_mu')
                    if self.gtgp_rice in ['-3', '-4', -3, None]:
                        self.total_rice = 0
                    self.gtgp_dry = return_values_2014(hh_row, 'gtgp_dry_mu')
                    if self.gtgp_dry in ['-3', '-4', -3, None]:
                        self.gtgp_dry = 0
                    self.age_1 = return_values_2014(hh_row, 'age')[0]
                    self.gender_1 = return_values_2014(hh_row, 'gender')[0]
                    self.education_1 = return_values_2014(hh_row, 'education')[0]
                    try:
                        self.land_area = return_values_2014(hh_row, 'gtgp_area')[i]
                    except:
                        pass
                    try:
                        self.non_gtgp_output = return_values_2014(hh_row, 'non_gtgp_output')[i]
                    except:
                        pass
                    if self.non_gtgp_output < 0:  # -2/-3/-4 values
                        self.non_gtgp_output = 0
                    try:
                        self.pre_gtgp_output = return_values_2014(hh_row, 'pre_gtgp_output')[i]
                    except:
                        pass
                    if self.pre_gtgp_output < 0:  # -2/-3/-4 values
                        self.pre_gtgp_output = 0
                    try:
                        self.land_time = return_values_2014(hh_row, 'non_gtgp_travel_time')[i]
                    except:
                        pass
                    try:
                        self.plant_type = return_values_2014(hh_row, 'non_gtgp_plant_type')[i]
                    except:
                        pass
                    try:
                        self.land_type = return_values_2014(hh_row, 'non_gtgp_land_type')[i]
                    except:
                        pass
                    self.hh_size = len(return_values_2014(hh_row, 'age'))
                    landpos = 0
                    self.gtgp_enrolled = 0
                    if self not in nongtgplist_2014:
                        nongtgplist_2014.append(self)
                    self.hh_row = hh_row
                    lp2014 = LandParcelAgent(hh_row, self, self.hh_id, self.hh_row, landpos, self.gtgp_enrolled,
                                             self.age_1, self.gender_1, self.education_1,
                                             self.gtgp_dry, self.gtgp_rice, self.total_dry, self.total_rice,
                                             self.land_type, self.land_time, self.plant_type, self.non_gtgp_output,
                                             self.pre_gtgp_output)

                    self.schedule.add(lp2014)
            except TypeError:  # NoneType
                pass


        # add gtgp
        for hh_row in agents2014:  # from excel_import

            try:
                for i in range(len(return_values_2014(hh_row, 'pre_gtgp_output'))):
                    hh_id = return_values_2014(hh_row, 'hh_id')
                    self.hh_id = hh_id
                    self.total_rice = return_values_2014(hh_row, 'non_gtgp_rice_mu')
                    if self.total_rice in ['-3', '-4', -3, None]:
                        self.total_rice = 0
                    self.total_dry = return_values_2014(hh_row, 'non_gtgp_dry_mu')
                    if self.total_dry in ['-3', '-4', -3, None]:
                        self.total_dry = 0
                    self.gtgp_rice = return_values_2014(hh_row, 'gtgp_rice_mu')
                    if self.gtgp_rice in ['-3', '-4', -3, None]:
                        self.total_rice = 0
                    self.gtgp_dry = return_values_2014(hh_row, 'gtgp_dry_mu')
                    if self.gtgp_dry in ['-3', '-4', -3, None]:
                        self.gtgp_dry = 0
                    self.age_1 = return_values_2014(hh_row, 'age')[0]
                    self.gender_1 = return_values_2014(hh_row, 'gender')[0]
                    self.education_1 = return_values_2014(hh_row, 'education')[0]
                    try:
                        self.land_area = return_values_2014(hh_row, 'gtgp_area')[i]
                    except:
                        pass
                    if self.land_area != 0:
                        self.land_type = 0
                    try:
                        self.pre_gtgp_output = return_values_2014(hh_row, 'pre_gtgp_output')[i]
                    except:
                        pass
                    if self.pre_gtgp_output < 0:  # -2/-3/-4 values
                        self.pre_gtgp_output = 0
                    try:
                        self.land_time = return_values_2014(hh_row, 'gtgp_travel_time')[i]
                    except:
                        pass
                    try:
                        self.plant_type = return_values_2014(hh_row, 'pre_gtgp_plant_type')[i]
                    except:
                        pass
                    try:
                        self.land_type = return_values_2014(hh_row, 'non_gtgp_land_type')[i]
                    except:
                        pass
                    self.hh_size = len(return_values_2014(hh_row, 'age'))
                    if self not in nongtgplist_2014 and self not in gtgplist2014:
                        gtgplist_2014.append(self)
                    self.gtgp_enrolled = 1
                    self.hh_row = hh_row
                    lp2014_gtgp = LandParcelAgent(hh_row, self, self.hh_id, self.hh_row, landpos, self.gtgp_enrolled,
                                                  self.age_1, self.gender_1, self.education_1,
                                                  self.gtgp_rice, self.total_dry, self.gtgp_dry, self.total_rice,
                                                  self.land_type, self.land_time, self.plant_type, self.non_gtgp_output,
                                                  self.pre_gtgp_output)
                    self.schedule.add(lp2014_gtgp)
            except TypeError:  # None
                pass

    def step(self):
        """Advance the model by one step"""
        self.datacollector.collect(self)
        self.datacollector2.collect(self)
        self.datacollector3.collect(self)
        self.datacollector4.collect(self)
        self.datacollector5.collect(self)
        self.datacollector6.collect(self)
        self.datacollector7.collect(self)
        self.datacollector8.collect(self)
        self.datacollector9.collect(self)
        self.datacollector10.collect(self)
        self.datacollector11.collect(self)
        self.datacollector12.collect(self)
        self.datacollector13.collect(self)

        self.datacollector14.collect(self)
        self.datacollector15.collect(self)
        self.datacollector16.collect(self)
        self.datacollector17.collect(self)
        self.datacollector18.collect(self)
        self.datacollector19.collect(self)
        self.datacollector20.collect(self)
        self.datacollector21.collect(self)
        self.datacollector22.collect(self)
        self.datacollector23.collect(self)
        self.datacollector24.collect(self)
        self.datacollector25.collect(self)
        self.datacollector26.collect(self)
        self.schedule.step()
