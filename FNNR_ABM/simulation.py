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

    try:
        if agent.slot == '':
            draw["Shape"] = "circle"
            draw["Color"] = "black"
            draw["Layer"] = 1

        if agent.slot == 1:
            draw["Shape"] = "circle"
            draw["Color"] = "green"
            draw["Layer"] = 2

    except:
        pass
    return draw

agent_canvas = SimpleCanvas(agent_draw, 700, 700)  # create simulation window

# create line graph
chart = ChartModule([{"Label": 'Animal Sightings',
                        "Color": "Black"}], canvas_height = 250, canvas_width = 700,
                        data_collector_name = 'datacollector')

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
                        "Animal Sightings", 100, 10, 10)

if __name__ == "__main__":
    server.port = 8521  # default
#    server.reset_model()
    server.launch()  # actual run line
    print('The simulation has been launched. Please check your web browser.')