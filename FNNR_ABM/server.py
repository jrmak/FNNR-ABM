# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from model import *
from SimpleContinuousModule import SimpleCanvas

def agent_draw(agent):
    draw = {"r": 1,
            "w": 1,
            "h": 1,
            "Filled": "true"}

# Household blue, individual green, land parcel yellow, PES policy unassigned

# admin_village is not actually important for drawing; it is a placeholder attribute to identify households
    try:
        if agent.admin_village == 1:
            draw["Shape"] = "rect"
            draw["Color"] = "blue"
            draw["Layer"] = 0
            draw["w"] = 0.01
            draw["h"] = 0.01

    except:
        pass
    try:
        if agent.GTGP_enrolled == 0:
            draw["Shape"] = "circle"
            draw["Color"] = "black"
            draw["Layer"] = 1
            draw["r"] = 3
        if agent.GTGP_enrolled == 1:
            draw["Shape"] = "circle"
            draw["Color"] = "gold"
            draw["Layer"] = 2
            draw["r"] = 3
    except:
        pass
    # else:
    #     draw["Color"] = "red"
    #     draw["Layer"] = 3
    #     draw["r"] = 3
    return draw

agent_canvas = SimpleCanvas(agent_draw, 700, 700)

chart = ChartModule([{"Label": 'Average Number of Migrants',
                    "Color": "Black"}], data_collector_name='datacollector')


#migrants = ABM(100, 10, 10)
#step
# migrants.datacollector.get_model_vars_dataframe().plot()

# The text elements below update with every step.

class Migrants(TextElement):
    def __init__(self):
        pass
    def render(self, model):
        return ("X-axis: migrants | Y-axis; steps (years) | ",
               "Average # of Migrants per Household: " + str(show_num_mig(model))
                )

class Individuals(TextElement):
    def __init__(self):
        pass
    def render(self, model):
        return ("Number of Marriages:" + ""  # to be replaced later with actual value
                )

text1 = Migrants()
text2 = Individuals()

server = ModularServer(ABM, [agent_canvas, chart, text1, text2], "GTGP Enrollment of Land Over Time",
                       100, 10, 10)

# if __name__ == "__main__":
server.launch()  # actual run line