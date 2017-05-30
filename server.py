from mesa.visualization.ModularVisualization import ModularServer

from model import ABM
from visualization_module import SimpleCanvas

def agent_draw(agent):
    draw = {"Shape": "circle",
            "r": 1,
            "Filled": "true"}

    if agent.GTGP_part == 1:
        draw["Color"] = "green"
        draw["Layer"] = 0
        draw["r"] = 1.5
    else:
        draw["Color"] = "black"
        draw["Layer"] = 1
        draw["r"] = 0.5
    return draw

agent_canvas = SimpleCanvas(agent_draw, 500, 500)

server = ModularServer(ABM, [agent_canvas], "Agents",
                       100, 10, 10)

server.launch()