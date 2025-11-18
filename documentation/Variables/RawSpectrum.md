---
title: RawSpectrum
kind: variable
source: Variables/RawSpectrum
last_updated: 2025-02-14
---

## Description
`RawSpectrum` is a numpy array with columns `[m/z, intensity]` representing a single Orbitrap MS2 scan. [`ms2_spectrum`](../Functions/ms2_spectrum.md) cleans and iteratively consumes this array to isolate Gaussian fragment peaks that survive intensity and quality filters.

## Code
```python
RawSpectrum = np.array([
    [150.0234, 1.2e4],
    [150.0250, 8.1e4],
    [150.0281, 4.5e4]
])
```

## Key operations
- Filtered to remove non-positive intensities before peak search.
- Passed to [`ms2_peakStats_safe`](../Functions/ms2_peakStats_safe.md) to estimate Gaussian peak properties around each local maximum.
- After a peak is accepted, the corresponding m/z window is removed so the next iteration can target lower-intensity fragments.

## Parameters
- Column 0 (`m/z`, Da): high-resolution mass axis.
- Column 1 (`intensity`, arbitrary units): ion counts or normalized intensity.

## Input
- Provided to [`ms2_spectrum`](../Functions/ms2_spectrum.md) from raw data loaders or mzML parsing utilities.

## Output
- Processed into fragment statistics and appended to [`ms2_spectrum`](../Functions/ms2_spectrum.md) results.

## Functions
- [`ms2_spectrum`](../Functions/ms2_spectrum.md)
- [`ms2_peakStats_safe`](../Functions/ms2_peakStats_safe.md)

## Called by
- Any loader producing MS2 spectra (e.g., `AllMS2Data`) before MS2-first feature construction.

## Example table

| m/z (Da) | intensity (a.u.) |
| --- | --- |
| 150.0234 | 12,000 |
| 150.0250 | 81,000 |
| 150.0281 | 45,000 |

These rows capture the fragment profile before Gaussian modeling.
