from agents import *
from model import *
from excel_import import *

if __name__ == "__main__":
    model = ABM(50, 10, 10) #(number of agents, grid width, grid height)
    N = 20 #number of steps
    for i in range(N):
        model.step()