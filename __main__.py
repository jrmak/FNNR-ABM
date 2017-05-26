from agents import *
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    model = ABM(50, 10, 10) #(number of agents, grid width, grid height)
    N = 20 #number of steps
    for i in range(N):
        model.step()
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content) #num of agents in each cell
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation='nearest')
    plt.colorbar()
    plt.show()