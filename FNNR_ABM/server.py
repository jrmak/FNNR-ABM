from mesa.visualization.ModularVisualization import ModularServer
from FNNR_ABM.model import ABM
from FNNR_ABM.SimpleContinuousModule import SimpleCanvas

def agent_draw(agent):
    draw = {"Shape": "circle",
            "r": 1,
            "Filled": "true"}

    if agent.GTGP_part_flag == 1:
        draw["Color"] = "green"
        draw["Layer"] = 0
        draw["r"] = 3
    else:
        draw["Color"] = "black"
        draw["Layer"] = 1
        draw["r"] = 3
    return draw

agent_canvas = SimpleCanvas(agent_draw, 700, 700)

server = ModularServer(ABM, [agent_canvas], "GTGP Enrollment of Land Over Time",
                       100, 10, 10)

server.launch()