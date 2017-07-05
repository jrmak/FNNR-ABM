# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from FNNR_ABM.model import *
from FNNR_ABM.SimpleContinuousModule import SimpleCanvas

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
                    "Color": "Black"}], canvas_height = 300, canvas_width = 750,
                    data_collector_name = 'datacollector')

# migrants = ABM(100, 10, 10)
# step here; non-working code for Mesa tables
# migrants.datacollector.get_model_vars_dataframe().plot()

# The text elements below update with every step.

class Map(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return ("Blue: Household agents | Black: non-GTGP land parcel agents | Yellow: GTGP land parcel agents"
                )


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
        return ("Total # of Marriages in Reserve: " + str(show_marriages(model))
                )

text0 = Map()
text1 = Migrants()
text2 = Individuals()

server = ModularServer(ABM, [agent_canvas, chart, text0, text1, text2], "GTGP Enrollment of Land Over Time",
                       100, 10, 10)

# if __name__ == "__main__":
server.launch()  # actual run line
