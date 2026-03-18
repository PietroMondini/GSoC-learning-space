# Review notes — PR #3522: Grass and Wolves as a PropertyLayer

**PR:** https://github.com/mesa/mesa/pull/3522  
**Author:** @PietroMondini (self)  
**Status:** 🔄 Draft (in progress)  
**Reviewer:** @quaquel, @souro26  
**Labels:** `GSoC: Not ready`

---

## What the PR does

Introduces two boolean `PropertyLayer` instances (`grass_layer`, `wolf_layer`) to track grass state and wolf positions as NumPy arrays. `GrassPatch` is refactored into a pure behavior agent — it retains ownership of the `get_eaten()` and `regrow()` scheduling logic, but its `fully_grown` state is removed and read/written directly from `self.model.grass_layer.data[x, y]`. `Sheep.move()` is updated to replace `cell.agents` iteration with direct NumPy index lookups over neighbor coordinates.

This is the follow-up to #3503, implementing the PropertyLayer architecture that @quaquel suggested during that review.

---

## Current status and open issues

The latest benchmark results (Mar 16) show a regression rather than improvement: 
WolfSheep small **+31.9%** and large **+68.5%** runtime. The PR is back in draft. 
The cause is likely the `wolf_layer` sync overhead — maintaining a full grid-sized boolean array 
in sync with wolf agent positions requires writing to the array on every wolf move, 
which may cost more than the iteration it saves.

Open questions before the PR is ready:
1. Is the wolf layer sync overhead worth it, or should `wolf_layer` be dropped and only `grass_layer`kept?
2. If `get_neighborhood_mask()` can't be used in the hot path, is there a way to cache or lazily
compute a local mask that avoids the full-array allocation?
3. Should wolf position tracking be removed entirely and grass-only vectorization be benchmarked
in isolation?

---

## What I learned 

**Sync cost is real and non-obvious.** When you move state from agents into a shared array,
you buy inexpensive reads, but you pay write costs on every state change. For grass, the sync cost is 
low. For wolf positions (which change every step for every wolf), the sync cost may dominate. 
The architecture has to match the access pattern.


