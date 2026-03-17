import numpy as np
from mesa.discrete_space import CellAgent


#TODO: Write docstrings
class Ant(CellAgent):
    """

    """
    def __init__(self, model, strength=np.arange(0.05,0.1), carry=0.0, cell=None):
        """"""
        super().__init__(model)
        self.cell = cell
        self.strength = strength
        self.carry = carry

    # TODO: define take_food from self.cell.food
    def take_food(self):...

    # TODO: define deposit_food from self.cell.food
    def deposit_food(self):...

    # TODO: define move from self.cell.neighbors
    def move(self):...

    # TODO: define a model step for an Ant
    def step(self):...
