# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from excel_export_summary_2014 import *
from SimpleContinuousModule import SimpleCanvas


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

class MapLegend(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        # image created on MS Paint and uploaded to internet, but also featured in this folder for reference
        return ("<img src = 'http://i64.tinypic.com/f41pwi.png'>" + "<br>"
                + "Non-GTGP Land Parcels: " + str(len(nongtgplist))
                + " | GTGP Land Parcels: " + str(len(gtgplist))
                + " | Total Land Parcels: " + str(len(nongtgplist) + len(gtgplist))
                + "<br><br></h3>")

text0 = MapLegend()
model = ABM(100, 10, 10)
server = ModularServer(ABM, [agent_canvas, text0],
                        "GTGP Enrollment of Land Over Time", 100, 10, 10)

if __name__ == "__main__":
    server.port = 8521  # default
#    server.reset_model()
    server.launch()  # actual run line