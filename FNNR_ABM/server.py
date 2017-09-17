# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from model import *
from agents import *
from excel_export_summary import *
from excel_export_summary_2014 import *
from excel_export_household import *
from excel_export_household_2014 import *
from SimpleContinuousModule import SimpleCanvas
import matplotlib.pyplot as plt


def agent_draw(agent):
    draw = {"r": 3,  # radius in pixels, for circles
            "w": 0.01,  # width in % of drawing window, for rectangles
            "h": 0.01,  # height in % of drawing window, for rectangles
            "Filled": "true"}

# Household blue, individual green, land parcel yellow, PES policy unassigned
# Will add legend later

# admin_village is not actually important to the model; it is a placeholder attribute to identify households
# so they can be drawn
# see model.py, line 179

    try:
        if agent.admin_village == 1:
            draw["Shape"] = "rect"
            draw["Color"] = "blue"
            draw["Layer"] = 0

    except:
        pass

# black if non-GTGP land parcel, yellow if GTGP

    try:
        if agent.gtgp_enrolled == 0:
            draw["Shape"] = "circle"
            draw["Color"] = "black"
            draw["Layer"] = 1

        if agent.gtgp_enrolled == 1:
            draw["Shape"] = "circle"
            draw["Color"] = "gold"
            draw["Layer"] = 2

    except:
        pass
    return draw

agent_canvas = SimpleCanvas(agent_draw, 700, 700)  # create simulation window

# create line graph
chart = ChartModule([{"Label": 'Average Number of Migrants',
                     "Color": "Black"}], canvas_height = 250, canvas_width = 700,
                     data_collector_name = 'datacollector')

chart2 = ChartModule([{"Label": 'Total # of Marriages in the Reserve',
                     "Color": "Black"}], canvas_height = 250, canvas_width = 700,
                     data_collector_name = 'datacollector2')


model = ABM(100, 10, 10)
erase_summary()
erase_household()
erase_household_2014()
erase_summary_2014()
initialize_household()
initialize_household_2014()
global i_counter
for i in range(81):  # sets up model to run for 80 steps
    model.step()
    i_counter = i
    save_summary(i_counter, show_cumulative_mig(model), show_instant_mig(model), show_instant_mig_per_hh(model),
                 show_cumulative_re_mig(model), show_instant_re_mig(model),                     \
                 show_instant_re_mig_per_hh(model), show_marriages(model), show_births(model), len(death_list),
                 show_num_labor(model), show_hh_size(model), show_income(model),
                 show_pop(model), show_gtgp_per_hh(model), show_non_gtgp_per_hh(model))
    save_summary_2014(i_counter, show_cumulative_mig_2014(model), show_instant_mig_2014(model),
                      show_instant_mig_per_hh_2014(model), show_cumulative_re_mig_2014(model),
                      show_instant_re_mig_2014(model), show_instant_re_mig_per_hh_2014(model),
                      show_marriages_2014(model), show_births_2014(model), len(death_list_2014),
                      show_num_labor_2014(model), show_hh_size_2014(model), show_income_2014(model),
                      show_pop_2014(model), show_gtgp_per_hh_2014(model), show_non_gtgp_per_hh_2014(model))

# 1 at the end of the variable name means that it's per year instead of accumulative
cumulative_out_mig_2016 = model.datacollector.get_model_vars_dataframe()  # see model.py
instant_out_mig_2016 = model.datacollector2.get_model_vars_dataframe()  # see model.py
cumulative_re_mig_2016 = model.datacollector3.get_model_vars_dataframe()
instant_re_mig_2016 = model.datacollector4.get_model_vars_dataframe()
marriage_2016 = model.datacollector5.get_model_vars_dataframe()
birth_2016 = model.datacollector6.get_model_vars_dataframe()
death_2016 = model.datacollector7.get_model_vars_dataframe()
pop_2016 = model.datacollector8.get_model_vars_dataframe()
gtgp_2016 = model.datacollector9.get_model_vars_dataframe()
non_gtgp_2016 = model.datacollector10.get_model_vars_dataframe()
hh_size_2016 = model.datacollector11.get_model_vars_dataframe()
num_labor_2016 = model.datacollector12.get_model_vars_dataframe()
income_2016 = model.datacollector13.get_model_vars_dataframe()

cumulative_mig_2014 = model.datacollector14.get_model_vars_dataframe()
instant_mig_2014 = model.datacollector15.get_model_vars_dataframe()
cumulative_re_mig_2014 = model.datacollector16.get_model_vars_dataframe()
instant_re_mig_2014 = model.datacollector17.get_model_vars_dataframe()
marriage_2014 = model.datacollector18.get_model_vars_dataframe()
birth_2014 = model.datacollector19.get_model_vars_dataframe()
death_2014 = model.datacollector20.get_model_vars_dataframe()
pop_2014 = model.datacollector21.get_model_vars_dataframe()
gtgp_2014 = model.datacollector22.get_model_vars_dataframe()
non_gtgp_2014 = model.datacollector23.get_model_vars_dataframe()
hh_size_2014 = model.datacollector24.get_model_vars_dataframe()
num_labor_2014 = model.datacollector25.get_model_vars_dataframe()
income_2014 = model.datacollector26.get_model_vars_dataframe()

instant_out_mig_2016.plot()
plt.title('Instant # of Out-Migrants in the Reserve (2016 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Migrants')

cumulative_re_mig_2016.plot()
plt.title('Cumulative # of Re-migrants in the Reserve (2016 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Re-migrants')

# instant_re_mig_2016.plot()
# plt.title('Instant # of Re-migrants in the Reserve (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Re-migrants')

# # household_out_mig_2016.plot()
# # plt.title('Average Number of Out-Migrants Per Household (2016 data)')
# # plt.xlabel('Years (Steps)')
# # plt.ylabel('# of Migrants')

# # household_re_mig_2016.plot()
# # plt.title('Average Number of Re-Migrants Per Household (2016 data)')
# # plt.xlabel('Years (Steps)')
# # plt.ylabel('# of Re-migrants')

# marriage_2016.plot()
# plt.title('Total # of Marriages in the Reserve (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Marriages')
#
# birth_2016.plot()
# plt.title('Total # of Births in the Reserve (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Births')
#
# death_2016.plot()
# plt.title('Total # of Deaths in the Reserve (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Deaths')
#
# pop_2016.plot()
# plt.title('Total Population in the Reserve (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('Population')

# gtgp_2016.plot()
# plt.title('Average # of GTGP Parcels Per Household (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('GTGP Parcels')
#
# non_gtgp_2016.plot()
# plt.title('Average # of Non-GTGP Parcels Per Household (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('Non-GTGP Parcels')
#
# hh_size_2016.plot()
# plt.title('Average Household Size (2016 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of People in Household')

num_labor_2016.plot()
plt.title('Average # of Laborers in Household (2016 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Laborers in Household')

income_2016.plot()
plt.title('Average Yearly Household Income (2016 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('Income (Yuan)')

# 2014

# cumulative_mig_2014.plot()
# plt.title('Cumulative # of Out-Migrants in the Reserve (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Migrants')

instant_mig_2014.plot()
plt.title('Instant # of Out-Migrants in the Reserve (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Migrants')

cumulative_re_mig_2014.plot()
plt.title('Cumulative # of Re-migrants in the Reserve (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Re-migrants')

instant_re_mig_2014.plot()
plt.title('Instant # of Re-Migrants in the Reserve (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Migrants')

# # household_mig_2014.plot()
# # plt.title('Average Number of Out-Migrants Per Household (2014 data)')
# # plt.xlabel('Years (Steps)')
# # plt.ylabel('# of Migrants')

# # household_re_mig_2014.plot()
# # plt.title('Average Number of Re-Migrants Per Household (2014 data)')
# # plt.xlabel('Years (Steps)')
#  #plt.ylabel('# of Re-migrants')
#
# marriage_2014.plot()
# plt.title('Total # of Marriages in the Reserve (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Marriages')
#
# birth_2014.plot()
# plt.title('Total # of Births in the Reserve (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Births')
#
# death_2014.plot()
# plt.title('Total # of Deaths in the Reserve (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Deaths')

pop_2014.plot()
plt.title('Total Population in the Reserve (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('Population')

# gtgp_2014.plot()
# plt.title('Average # of GTGP Parcels Per Household (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('GTGP Parcels')
#
# non_gtgp_2014.plot()
# plt.title('Average # of Non-GTGP Parcels Per Household (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('Non-GTGP Parcels')

# hh_size_2014.plot()
# plt.title('Average Household Size (2014 data)')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of People in Household')

num_labor_2014.plot()
plt.title('Average # of Laborers in Household (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Laborers in Household')

income_2014.plot()
plt.title('Average Yearly Household Income (2014 data)')
plt.xlabel('Years (Steps)')
plt.ylabel('Income (Yuan)')

plt.show() # comment or uncomment this line to see or hide the graphs

# The text elements below update with every step.


class MapLegend(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        # image created on MS Paint and uploaded to internet, but also featured in this folder for reference
        return ("<img src = 'http://i64.tinypic.com/f41pwi.png'>" + "<br>"
                + "Non-GTGP Land Parcels: " + str(len(nongtgplist))
                + " | GTGP Land Parcels: " + str(len(gtgplist))
                + " | Total Land Parcels: " + str(len(nongtgplist) + len(gtgplist))
                + " | Step: " + str(i_counter)
                + "<br><br></h3>")

# text0 = MapLegend()
#
# server = ModularServer(ABM, [agent_canvas, text0],
#                         "GTGP Enrollment of Land Over Time", 100, 10, 10)
#
# if __name__ == "__main__":
#     server.port = 8521  # default
#     server.launch()  # actual run line
