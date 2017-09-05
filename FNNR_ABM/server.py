# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
Currently: the two example graphs for migration and marriage that pop up (static, 100 steps, made with matplotlib)
are the same as the two graphs in the web browser simulation (dynamic number of steps, made with Mesa/Charts.js).
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from model import *
from agents import *
from excel_export_summary import *
from excel_export_household import *
from excel_export_household_2014 import *
from SimpleContinuousModule import SimpleCanvas
import matplotlib.pyplot as plt
import inspect


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
initialize_household()
erase_household_2014()
initialize_household_2014()
global i_counter
for i in range(100):  # sets up model to run for 80 steps
    model.step()
    i_counter = i
    save_summary(i_counter, show_num_mig(model), show_num_mig_per_year(model), show_re_mig(model),                     \
                 show_re_mig_per_year(model), show_marriages(model), show_births(model), len(death_list),
                 show_num_labor(model), show_hh_size(model), show_income(model),
                 show_pop(model), show_gtgp_per_hh(model), show_non_gtgp_per_hh(model))
# 1 at the end of the variable name means that it's per year instead of accumulative
mig_plot = model.datacollector.get_model_vars_dataframe()  # see model.py
re_mig_plot = model.datacollector2.get_model_vars_dataframe()
mig_plot1 = model.datacollector3.get_model_vars_dataframe()  # see model.py
re_mig_plot1 = model.datacollector4.get_model_vars_dataframe()
mar_plot = model.datacollector5.get_model_vars_dataframe()
bir_plot = model.datacollector6.get_model_vars_dataframe()
dea_plot = model.datacollector7.get_model_vars_dataframe()
mar_plot1 = model.datacollector8.get_model_vars_dataframe()
bir_plot1 = model.datacollector9.get_model_vars_dataframe()
dea_plot1 = model.datacollector10.get_model_vars_dataframe()
pop_plot = model.datacollector11.get_model_vars_dataframe()
gtgp_plot = model.datacollector12.get_model_vars_dataframe()
non_gtgp_plot = model.datacollector13.get_model_vars_dataframe()
hh_size_plot = model.datacollector14.get_model_vars_dataframe()
num_labor_plot = model.datacollector15.get_model_vars_dataframe()

mig_plot.plot()
plt.title('Instant # of Out-Migrants in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Migrants')

re_mig_plot.plot()
plt.title('Cumulative # of Re-migrants in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Re-migrants')

mig_plot1.plot()
plt.title('Average Number of Out-Migrants Per Household')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Migrants')
#
# re_mig_plot1.plot()
# plt.title('Average Number of Re-Migrants Per Household')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Re-migrants')

mar_plot.plot()
plt.title('Total # of Marriages in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Marriages')

bir_plot.plot()
plt.title('Total # of Births in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Births')

dea_plot.plot()
plt.title('Total # of Deaths in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Deaths')

# mar_plot1.plot()
# plt.title('Marriages in the Reserve, Per Year')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Marriages')
#
# bir_plot1.plot()
# plt.title('Births in the Reserve, Per Year')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Births')
#
# dea_plot1.plot()
# plt.title('Deaths in the Reserve, Per Year')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Deaths')

pop_plot.plot()
plt.title('Total Population in the Reserve')
plt.xlabel('Years (Steps)')
plt.ylabel('Population')

gtgp_plot.plot()
plt.title('Average # of GTGP Parcels Per Household')
plt.xlabel('Years (Steps)')
plt.ylabel('GTGP Parcels')

non_gtgp_plot.plot()
plt.title('Average # of Non-GTGP Parcels Per Household')
plt.xlabel('Years (Steps)')
plt.ylabel('Non-GTGP Parcels')

hh_size_plot.plot()
plt.title('Average Household Size')
plt.xlabel('Years (Steps)')
plt.ylabel('# of People in Household')

num_labor_plot.plot()
plt.title('Average # of Laborers in Household')
plt.xlabel('Years (Steps)')
plt.ylabel('# of Laborers in Household')


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

#+ "<h3>Average # of Migrants per Household

class Migrants(TextElement):
    # not used below
    def __init__(self):
        pass

    def render(self, model):
        return ("X-axis: migrants | Y-axis: steps (years) | ",
                "Average # of Migrants per Household: " + str(show_num_mig(model))
                + "<br><br>"
                + "<h3>Total # of Marriages in the Reserve</h3>")


class Marriages(TextElement):
    # not used below
    def __init__(self):
        pass

    def render(self, model):
        return ("X-axis: marriages | Y-axis: steps (years) | ",
                "Total # of Marriages in the Reserve: " + str(show_marriages(model))
                )

text0 = MapLegend()
text1 = Migrants()  # not used below
text2 = Marriages()  # not used

# server = ModularServer(ABM, [agent_canvas, text0],
#                        "GTGP Enrollment of Land Over Time", 100, 10, 10)

# if __name__ == "__main__":
# server.port = 8521  # default
# server.launch()  # actual run line
