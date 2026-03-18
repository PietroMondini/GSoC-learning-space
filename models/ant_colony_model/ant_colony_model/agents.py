import math

import numpy as np
from mesa.discrete_space import CellAgent, FixedAgent
from mesa.time import Schedule
from networkx.algorithms.distance_measures import radius
from networkx.classes import neighbors


class Ant(CellAgent):
    """
    An Ant that searches for food and follows pheromone trails.

    Takes food from piles and deposits it in the nest.

    Attributes:
        cell (Cell): The cell in the grid where the ant is located.
        strength (int): The strength of the ant.
        carry (int): The amount of food the ant is carrying.
    """

    def __init__(self, model, carry=0, cell=None, spread_pheromones_radius=2):
        """Initialize a new ant agent.

        Args:
            model (Model): The model instance this ant belongs to.
            carry (int): The amount of food currently being carried. Defaults to 0.0.
            cell (Cell): The initial cell location for the ant. Defaults to None.
        """
        super().__init__(model)
        self.cell = cell
        self.strength = self.random.randrange(5, 15, 1)
        self.carry = carry
        self.pheromones_spread_radius = spread_pheromones_radius

    def step(self):
        """
        Execute one step of the agent's behavior.

        Args:
            self (Ant): The current agent instance.
        """
        self.move()

        # If carrying food and just moved to the nest, deposit it
        if self.carry > 0 and self.cell == self.model.nest.cell:
            self.deposit_food()
            return

        # If not carrying food and just moved in a cell with food, take it
        if self.cell != self.model.nest.cell and self.carry == 0 and self.cell.food > 0:
            self.take_food()
            self.spread_pheromones()
            return

    def move(self):
        """
        Move to a neighboring cell based on pheromone and nest scent levels.
        """
        neighborhood = self.cell.neighborhood

        pheromones, nest_scent = zip(*[(n.pheromones, n.nest_scent) for n in neighborhood])

        if self.carry > 0.:
            self.cell = neighborhood.select(lambda n: n.nest_scent == max(nest_scent)).select_random_cell()
            self.spread_pheromones()
        else:
            self.cell = neighborhood.select(lambda n: n.pheromones == max(pheromones)).select_random_cell()

    def take_food(self):
        """
        Take as much food as possible from the current cell.

        Args:
            self (Ant): The current agent instance.

        Returns:
            float: The amount of food that was taken.
        """
        x = min(self.cell.food, self.strength)
        self.cell.food = self.cell.food - x
        self.carry += x
        return x

    def deposit_food(self):
        """
        Deposit all carried food into the current cell.

        Args:
            self (Ant): The current agent instance.

        Returns:
            float: The amount of food that was deposited.
        """
        x = self.carry
        self.cell.food += x
        self.carry = 0
        return x

    def spread_pheromones(self):
        """ Spread pheromones from the current cell to its neighbors to a radius of self.pheromones_spread_radius."""
        neighborhood = self.cell.get_neighborhood(self.pheromones_spread_radius, include_center=True)
        coords = np.array([c.coordinate for c in neighborhood])
        xs, ys = coords[:, 0], coords[:, 1]

        cx, cy = self.cell.coordinate

        dist = np.abs(np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2))
        ph_values = 1.0 - dist / self.pheromones_spread_radius

        new_values = np.minimum(1.0, self.model.grid.pheromones.data[xs, ys] + ph_values)

        self.model.grid.pheromones.data[xs, ys] = np.maximum(
            self.model.grid.pheromones.data[xs, ys],
            new_values,
        )


class Nest(FixedAgent):
    """A nest that serves as the home base for a colony of ants.

    The nest is placed at the center of the grid and periodically releases ants
    to forage for food.

    Attributes:
        cell: The cell in the grid where the nest is located.
        ants (int): Total number of ants in the nest.
        ant_per_step (int): Number of ants released per step in the model's event schedule.
    """

    def __init__(self, model, ants=50, ant_per_step=5, pheromones_spread_radius=2):
        """Initialize a new nest instance.

        Args:
            model: The model instance that controls the environment and simulation.
            ants (int): Total number of ants in the nest. Defaults to 50.
            ant_per_step (int): Number of ants to release per step in the model's
                event schedule. Defaults to 5.
        """

        super().__init__(model)
        self.cell = self.model.grid.find_nearest_cell(np.array([self.model.height/2, self.model.width/2]))
        self.ants = ants
        self.ant_per_step = ant_per_step
        self.pheromones_spread_radius = pheromones_spread_radius

        self.release_ants()
        self.model.schedule_recurring(self.release_ants, Schedule(interval=1, count=None))

    def release_ants(self):
        Ant.create_agents(
            self.model,
            min(self.ants, self.ant_per_step),
            spread_pheromones_radius=self.pheromones_spread_radius,
            cell=self.cell,
        )
        self.ants -= min(self.ants, self.ant_per_step)

    def food(self):
        return self.cell.food