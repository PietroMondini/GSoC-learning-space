# Ant Colony Model (ACM)

A Mesa replication of the classic [NetLogo Ants model](https://ccl.northwestern.edu/netlogo/models/Ants) by Uri Wilensky (1997), simulating emergent foraging behavior in an ant colony through pheromone-based communication.

---

## What the model does

Ants are released from a central nest and explore a grid in search of food. 
When an ant finds food, it picks up as much as its strength allows and returns to the nest,  
laying a pheromone trail along the way. Other ants follow the strongest pheromone gradient when 
 searching and follow the nest-scent gradient when returning home. Pheromones evaporate each step,
so trails naturally fade if food runs out. 
Food is distributed in `N` circular piles arranged symmetrically around the nest.

The key emergent behavior is collective intelligence: no ant has a global map, 
yet the colony efficiently locates and depletes food sources through local gradient-following alone.

---

## Mesa features used

| Feature | How it's used |
|---|---|
| `OrthogonalMooreGrid` | 2D grid with Moore neighborhoods for agent movement |
| `PropertyLayer` | Three layers: `pheromones` (float), `food` (int), `nest_scent` (float) |
| `CellAgent` / `FixedAgent` | `Ant` as a mobile `CellAgent`; `Nest` as a stationary `FixedAgent` |
| `Scenario` | `AntScenario` holds all model parameters, integrates cleanly with the SolaraViz sliders |
| `SolaraViz` + `SpaceRenderer` | Interactive browser visualization with agent and PropertyLayer overlays |

---

## Model parameters

| Parameter | Default | Description |
|---|---------|---|
| `width` / `height` | 50      | Grid dimensions |
| `ants` | 200     | Total ants released over the simulation |
| `ants_per_step` | 20      | Ants released from the nest each step |
| `pheromones_spread_radius` | 8       | Radius (in cells) of pheromone deposit around an ant |
| `food_piles` | 4       | Number of food sources |
| `food_radius` | 2       | Radius of each food pile in cells |
| `seed` | 1       | Random seed |

---

## How to run

Install mesa:

```bash
pip install mesa[rec]
```

Launch the interactive visualization:

```bash
solara run app.py
```

---

## Future improvements

- **Pheromone evaporation rate** as a parameter.
- **Greedy behaviour**, I want to add some type of greedy behavior to the ants, like if they have 
food near them, they will go for it.
- **Strength as a distribution parameter.** Ant strength is drawn uniformly from `[5, 15)` 
with no scenario-level control.
- **Directional movement.** Ants right now can move in any direction, but I want to add a 
directional bias to the random choice of a neighbor cell.
- **Nest reproduction.** I want to add a nest reproduction mechanism, so that when ants go enough far 
away from the nest, they can create a new nest, modifying also the nest scent layer mechanism.
- **Other forms of food distribution.** I want to add a more complex food distribution mechanism,
not only circular distribution (and maybe even dynamical).

---

## References

Wilensky, U. (1997). NetLogo Ants model. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL. https://ccl.northwestern.edu/netlogo/models/Ants
