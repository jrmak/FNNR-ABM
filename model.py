from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from agents import HouseholdAgent

class ABM(Model):
    """Handles agent creation, placement, and value changes"""
    def __init__(self, n_agents, width, height):
        self.num_agents = n_agents
        self.space = ContinuousSpace(width, height, True, grid_width = 10, grid_height = 10)
        #class space.ContinuousSpace(x_max, y_max, torus, x_min=0, y_min=0, grid_width=100, grid_height=100)
        #methods: get_distance, get_neighbors, move_agent, out_of_bounds, place_agent
        self.schedule = RandomActivation(self)
        self.make_agents()
        self.running = True

    #Create agents
    def make_agents(self):
        """Create the household agents"""
        #for i in hh_id_list
            #x = imported latitude
            #y = imported longitude
        #pos = (x,y)
        #hh = HouseholdAgent(i, self, pos, self.GTGP_part, self.f_age, self.GTGP_land,
        #                    self.GTGP_coef, self.mig_prob, self.num_mig, self.min_req_labor,
        #                    self.num_labor)
        self.space.place_agent(hh, pos)
        self.schedule.add(hh)

    def step(self):
        """Advance the model by one step"""
        self.schedule.step()