"""
ACM - Ant Colony Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Ants model.
    https://ccl.northwestern.edu/netlogo/models/Ants.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import math

from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.scenarios import Scenario

from agents import Ant

class AntScenario(Scenario):
    """Scenario parameters for the Ants model.

    Args:
        height: Grid height
        width: Grid width
        ants: Number of ants
        food_piles: Number of food piles
        rng: Random rng
    """
    width = 50
    height = 50
    ants = 40
    food_piles = 3
    rng = 1

class AntModel(Model):
    """
     Ants Colony Model.

     A model for simulating the behavior of ants in a colony searching for food.
    """

    description = (
        "A model for simulating the behavior of ants in a colony searching for food."
    )

    def __init__(self, scenario=None):
        """
        Initializes the simulation model with grid, parameters, and agents.

        :param scenario: Scenario configuration object containing required parameters
            like grid dimensions (height, width), number of ants, and food piles.
        :type scenario: Scenario
        """

        if scenario is None:
            scenario = AntScenario()

        super().__init__(scenario=scenario)

        # Initialize the model parameters
        self.height = scenario.height
        self.width = scenario.width

        # Create a grid using an OrthogonalMooreGrid
        self.grid = OrthogonalMooreGrid(
            [self.height, self.width],
            capacity=math.inf,
            random=self.random,
            )

        # Create the nest cell in the center of the grid
        self.nest_cell = self.grid.coord_to_cell((self.height // 2, self.width // 2))

        # Create PropertyLayers for pheromones, food, and nest 'scent'.
        self.grid.create_property_layer(
            'pheromones',
            default_value=0.0,
            dtype=float,
        )

        self.grid.create_property_layer(
            'food',
            default_value=0,
            dtype=int,
        )

        self.grid.create_property_layer(
            'nest_scent',
            default_value=0.0,
            dtype=float,
        )

        #TODO: Setting up nest_scent as a gradient of distance from the nest cell

        #TODO: Set up data collection

        # Create Ants:
        Ant.create_agents(
            self,
            scenario.ants,
            cell = self.random.choice(
                self.grid.all_cells.cells, k=scenario.ants
            ),
        )

        # Set up the food piles layer.


        # Set up the nest scent layer.


        #TODO: Collect initial data

    def step(self):
        """Execute one step of the model."""
        # Activate ants
        self.agents_by_type[Ant].shuffle_do("step")

        # TODO: Collect data







