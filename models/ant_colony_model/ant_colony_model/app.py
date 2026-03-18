from model import AntModel, AntScenario
from agents import Ant, Nest

from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
)
from mesa.visualization.components import AgentPortrayalStyle, PropertyLayerStyle


# ---------------------------------------------------------------------------
# Agent portrayal
# ---------------------------------------------------------------------------

def ant_colony_portrayal(agent):
    if agent is None:
        return None

    if isinstance(agent, Nest):
        return AgentPortrayalStyle(
            marker="*",
            size=300,
            color="gold",
            zorder=4,
        )

    if isinstance(agent, Ant):
        return AgentPortrayalStyle(
            marker="o",
            size=30,
            color="saddlebrown" if agent.carry > 0 else "black",
            zorder=3,
        )
    return None

# ---------------------------------------------------------------------------
# PropertyLayer overlay component
# ---------------------------------------------------------------------------

def property_layers_portrayal(pl):
    """
    Renders pheromones and food PropertyLayers as heatmap overlays,
    plus a gold star marking the nest position.
    """
    # Blue pheromones
    if pl.name == "pheromones":
        return PropertyLayerStyle(
            color="blue", alpha=0.5, colorbar=False
        )
    # Green food
    if pl.name == "food":
        return PropertyLayerStyle(
            color="green", alpha=1, colorbar=False
        )
    return None

    # Green food

# ---------------------------------------------------------------------------
# Post-process hooks
# ---------------------------------------------------------------------------

def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Ant Colony", fontsize=10)

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------

model_params = {
    "rng": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "ants": Slider("Number of Ants", 50, 10, 200, 10),
    "ants_per_step": Slider("Ants per Step", 1, 1, 10),
    "food_piles": Slider("Food Piles", 3, 1, 8),
    "food_radius": Slider("Food Pile Radius", 3, 1, 10),
    "pheromones_spread_radius": Slider("Pheromone Spread Radius", 2, 1, 8),
}

# ---------------------------------------------------------------------------
# Space renderer
# ---------------------------------------------------------------------------

model = AntModel(scenario=AntScenario())

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
).setup_agents(ant_colony_portrayal).setup_propertylayer(property_layers_portrayal)

renderer.post_process = post_process_space

# Attach the layer overlay to the renderer's post-process hook
_original_post = renderer.post_process

def _combined_post(ax):
    _original_post(ax)

renderer.post_process = _combined_post
renderer.draw_propertylayer()
renderer.draw_agents()

# ---------------------------------------------------------------------------
# SolaraViz page
# ---------------------------------------------------------------------------

page = SolaraViz(
    model,
    renderer,
    name="Ant Colony Model",
)
page  # noqa