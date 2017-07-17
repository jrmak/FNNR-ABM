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


# model = ABM(100, 10, 10)
# for i in range(100):  # sets up model to run for 100 steps
#     model.step()
# mig_plot = model.datacollector.get_model_vars_dataframe()  # see model.py
# mar_plot = model.datacollector2.get_model_vars_dataframe()
# # migranttable = migrants.datacollector.get_agent_vars_dataframe()
# # migranttable.head()
# # TypeError: '<' not supported between instances of 'LandParcelAgent' and 'int'
# mig_plot.plot()
# plt.title('Average Number of Out-Migrants Per Household')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Migrants')
#
# mar_plot.plot()
# plt.title('Total # of Marriages in the Reserve')
# plt.xlabel('Years (Steps)')
# plt.ylabel('# of Marriages')
#
# plt.show()

# The text elements below update with every step.


class MapLegend(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        # image created on MS Paint and uploaded to internet, but also featured in this folder for reference
        return ("<img src = 'http://i64.tinypic.com/f41pwi.png'>" + "<br>"
                + "Non-GTGP Land Parcels: " + str(len(nongtgplist))
                + " | GTGP Land Parcels: " + str(len(gtgplist))
                + " | Total Land Parcels: 361"
                + "<br><br>"
                + "<h3>Average # of Migrants per Household</h3>")
        # return ("Blue: Household agents | Black: non-GTGP land parcel agents | Yellow: GTGP land parcel agents"
        #         )


class Migrants(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return ("X-axis: migrants | Y-axis: steps (years) | ",
                "Average # of Migrants per Household: " + str(show_num_mig(model))
                + "<br><br>"
                + "<h3>Total # of Marriages in the Reserve</h3>")


class Marriages(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return ("X-axis: marriages | Y-axis: steps (years) | ",
                "Total # of Marriages in the Reserve: " + str(show_marriages(model))
                )

text0 = MapLegend()
text1 = Migrants()
text2 = Marriages()

server = ModularServer(ABM, [agent_canvas, text0, chart, text1, chart2, text2],
                       "GTGP Enrollment of Land Over Time", 100, 10, 10)

# if __name__ == "__main__":
server.launch()  # actual run line
