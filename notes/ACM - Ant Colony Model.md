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