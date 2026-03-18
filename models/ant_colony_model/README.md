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

### Why this model

Ant foraging is a canonical example of stigmergic coordination agents communicate indirectly 
through the environment rather than directly with each other. 
It's one of the best demonstrations of the gap between individual simplicity and collective complexity,
which is exactly what ABM is built to study. It also exercises a broad range of 
Mesa features simultaneously, making it a good learning vehicle.

---

## What I learned building it

**PropertyLayers as the environment, not agents.** The natural instinct when reading about "pheromones"
is to model them as agent state but Mesa's `PropertyLayer` is the right abstraction. 
Pheromones, food, and nest scent are spatial fields, not agent attributes. 
Keeping them on the grid makes the physics (diffusion, evaporation, gradient queries) 
cheap and explicit.

**Vectorizing spatial setup with NumPy.** Both `setup_food_circle` and `setup_nest_scent` build 
the entire grid layer in a handful of NumPy array operations rather than nested loops. 
Using `np.meshgrid` with `indexing="ij"` to generate coordinate arrays and broadcasting for 
distance/mask computation was the right approach — and meaningfully faster on larger grids.

**Pheromone spreading with index arrays.** `spread_pheromones` collects neighborhood coordinates into 
a NumPy array and indexes `PropertyLayer.data` directly with `[xs, ys]`. This avoids iterating over 
`CellCollection` and keeps the per-ant update vectorized. One subtle point: `PropertyLayer.data` 
returns a `memoryview`, so wrapping with `np.asarray()` is required when doing arithmetic comparisons.

**`FixedAgent` + `schedule_recurring` for the nest.** Modeling the nest as a `FixedAgent` 
that schedules its own `release_ants` callback cleanly separates colony-level logic from ant-level 
logic. The nest manages its budget; the ants handle their own movement. Neither needs to know the 
other's internals.

**Movement as a greedy gradient ascent.** Ants don't pathfind they just pick the neighbor with the 
highest relevant signal (pheromones when foraging, nest scent when returning). This local rule 
produces globally coherent trails. It's a good reminder that emergent behavior doesn't require 
complex agent cognition.

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
