# Peer review — PR #3545: add rescale helper to scenario

**PR:** https://github.com/mesa/mesa/pull/3545  
**Author:** @souro26  
**Status:** ✅ Merged (Mar 16, 2026) 
**Reviewers:** @quaquel, @EwoutH, @PietroMondini
**Labels:** `enhancement`

---

## What the PR does

Adds a `rescale_samples(samples, ranges)` helper function to `mesa/experimental/scenarios/scenario.py`.
The function maps a QMC sample matrix from [0, 1] to user-defined parameter ranges using vectorized
NumPy broadcasting. Intended to be called before `Scenario.from_ndarray()` when parameter samples 
need to be mapped to meaningful value ranges.

Core implementation:
```python
mins = ranges[:, 0]
scale = ranges[:, 1] - mins
return samples * scale + mins  # or in-place equivalent
```

---

## Design observations

### Placement is correct

Keeping this as a standalone module-level function rather than a `Scenario` method is the right call.
Rescaling is a preprocessing step on the raw sample matrix it happens before scenarios are constructed,
so it doesn't belong on the class. A standalone function is also easier to test and use independently
of Mesa's scenario machinery.

---

## Test coverage gaps

The existing tests cover basic scaling, negative ranges, and dimension mismatches. One case worth adding may be:

**1. `inplace=False` leaves the original unmodified.**  
Currently there is no assertion that the input array is unchanged after a non-in-place call. This should be explicit:

```python
def test_rescale_does_not_mutate_input():
    original = np.array([[0.0, 0.5, 1.0]])
    original_copy = original.copy()
    ranges = np.array([[0, 10], [0, 20], [-1, 1]])
    rescale_samples(original, ranges, inplace=False)
    np.testing.assert_array_equal(original, original_copy)
```

