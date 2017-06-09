# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
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
        if agent.GTGP_part_flag == 0:
            draw["Shape"] = "circle"
            draw["Color"] = "black"
            draw["Layer"] = 1
            draw["r"] = 3
        if agent.GTGP_part_flag == 1:
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

# set webpage header here
server = ModularServer(ABM, [agent_canvas, chart], "GTGP Enrollment of Land Over Time",
                       100, 10, 10)

server.launch()  # actual run line