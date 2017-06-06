from mesa.visualization.ModularVisualization import ModularServer
from model import ABM
from SimpleContinuousModule import SimpleCanvas

def agent_draw(agent):
    draw = {"Shape": "circle",
            "r": 1,
            "Filled": "true"}

#Household blue, individual green, land parcel yellow, PES policy unassigned

    try:
        if agent.admin_village == 1:
            draw["Color"] = "blue"
            draw["Layer"] = 0
            draw["r"] = 3
    except:
        pass
    try:
        if agent.GTGP_part_flag == 0:
            draw["Color"] = "black"
            draw["Layer"] = 1
            draw["r"] = 3
        if agent.GTGP_part_flag == 1:
            draw["Color"] = "gold"
            draw["Layer"] = 2
            draw["r"] = 3
    except:
        pass
    #else:
    #    draw["Color"] = "red"
    #    draw["Layer"] = 3
    #    draw["r"] = 3
    return draw


agent_canvas = SimpleCanvas(agent_draw, 700, 700)

server = ModularServer(ABM, [agent_canvas], "GTGP Enrollment of Land Over Time",
                       100, 10, 10)

server.launch()