# Review notes — PR #3503: Optimise Wolf-sheep performance

**PR:** https://github.com/mesa/mesa/pull/3503  
**Author:** @PietroMondini (self)  
**Status:** ✅ Merged (Mar 12, 2026)  
**Reviewer:** @quaquel  
**Labels:** `performance`, `example`

---

## What the PR does

Replaces the two separate `CellCollection.select()` passes in `Sheep.move()` with a single manual loop using an early-exit strategy. The original code made two full iteration passes over the neighborhood on every agent step — one to filter wolf-free cells, one to find grass. The new code combines both checks into a single loop, breaking out of the inner agent iteration as soon as a wolf is detected in a cell.

**Result:** ~15–25% runtime reduction on WolfSheep (small and large), with no meaningful impact on other models.

---

## What I learned from this review

**Single ojective PRs.** Splitting the work into "early-exit now, PropertyLayer later" was 
the right call. A PR that only does one thing is easier to review, easier to revert if it causes 
problems, and provides a clean benchmark baseline. 
Trying to ship both changes in a single PR would have made the benchmark results harder to 
interpret and the review harder to follow.

**On early-exit as a pattern.** The optimization itself is straightforward, but it requires 
understanding that `cell.agents` is an iterable of arbitrary agent types, 
and that checking `isinstance(agent, Wolf)` is O(1) per agent. 
The original `CellCollection.select()` abstraction hides this it's clean but forces two passes.
The tradeoff is readability vs. performance.

---

## What I'd do differently

The PR description could have included a brief code snippet showing the before/after
to make the improvement immediately scannable without needing to read the diff. 
The benchmark table conveys *that* it's faster, but a two-line before/after would convey 
*why* in 10 seconds. Worth doing for future PRs.
