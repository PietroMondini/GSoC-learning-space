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

import numpy as np
from mesa import Model, DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.experimental.scenarios import Scenario

from agents import Ant, Nest


class AntScenario(Scenario):
    """Scenario parameters for the Ants model.

    Args:
        height: Grid height
        width: Grid width
        ants: Number of ants
        ants_per_step: Number of ants released per step
        pheromones_spread_radius: Pheromones spread radius
        food_piles: Number of food piles
        seed: Random rng
    """
    width = 50
    height = 50
    ants = 200
    ants_per_step = 20
    pheromones_spread_radius = 8
    food_piles = 4
    food_radius = 2.0
    seed = 1

class AntModel(Model):
    """
     Ants Colony Model.

     A model for simulating the behavior of ants in a colony searching for food.
    """

    description = (
        "A model for simulating the behavior of ants in a colony searching for food."
    )

    def __init__(self, scenario=None):
        """Initialize the simulation model with grid, parameters, and agents.

        Args:
            scenario (Scenario): Scenario configuration object containing required
                parameters like grid dimensions (height, width), number of ants,
                and food piles. Defaults to AntScenario().
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
        self.nest = Nest(self, scenario.ants, scenario.ants_per_step, scenario.pheromones_spread_radius)

        # Create PropertyLayers for pheromones, food, and nest 'scent'.
        self.grid.create_property_layer(
            'pheromones',
            default_value=0.0,
            dtype=float,
        )

        self.setup_food_circle(scenario.food_piles, food_radius=scenario.food_radius)

        self.setup_nest_scent()

        model_reporters = {
            "Ants": lambda m: len(m.agents_by_type[Ant]),
            "Total Food": lambda m: m.grid.food.data.sum(),
        }

        self.datacollector = DataCollector(model_reporters)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Execute one step of the model."""
        # Pheromone dissipation
        self.grid.pheromones.data = np.maximum(0.0, self.grid.pheromones.data - 0.2)

        # Activate ants
        self.agents_by_type[Ant].shuffle_do("step")

        self.datacollector.collect(self)

    def setup_food_circle(self, n, radius=0.8, food_radius=0.0):
        """
        Creates a PropertyLayer for food sources in the grid.

        Places n food piles evenly distributed around a circle (like clock positions)
        on the grid's food PropertyLayer.

        Args:
            n (int):          Number of food piles to create.
            radius (float):   Radius of the circle as a proportion of grid size.
            food_radius (float): Radius of each food pile in cells.
        """
        self.grid.create_property_layer("food", default_value=0, dtype=int)
        food = self.grid.food

        center_x, center_y = self.nest.cell.coordinate
        grid_radius = radius * min(self.width, self.height) / 2

        xs, ys = np.meshgrid(
            np.arange(self.width),
            np.arange(self.height),
            indexing="ij",
        )

        for i in range(n):
            angle = 2 * math.pi * i / n
            fx = math.ceil(center_x + grid_radius * math.cos(angle))
            fy = math.ceil(center_y + grid_radius * math.sin(angle))

            mask = (xs - fx) ** 2 + (ys - fy) ** 2 <= food_radius ** 2
            food.data[mask] += self.rng.integers(5, 26, size=mask.sum())

    def setup_nest_scent(self):
        """
        Creates a PropertyLayer for nest scent.

        Scent is highest at the nest centre and decreases with distance,
        reaching 0 at the grid edges.
        """
        self.grid.create_property_layer("nest_scent", default_value=0.0, dtype=float)
        nest_scent = self.grid.nest_scent

        cx, cy = self.nest.cell.coordinate

        xs, ys = np.meshgrid(
            np.arange(self.width),
            np.arange(self.height),
            indexing="ij",
        )

        dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
        max_dist = np.sqrt(cx ** 2 + cy ** 2)  # distance from nest to corner

        nest_scent.data[:] = np.maximum(0.0, 1.0 - dist / max_dist)


