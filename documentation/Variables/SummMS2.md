---
title: SummMS2
kind: table
source: Variables/SummMS2
last_updated: 2025-02-14
---

## Description
`SummMS2` stores redundancy-resolved MS2 detections. Each row describes a precursor targeted by the instrument, along with RT umbrellas, intensity statistics, and IDs linking back to raw spectra. It is produced by [`AllMS2Data`](../Functions/AllMS2Data.md) when parsing raw vendor files or by [`ms2_SpectralRedundancy`](../Functions/ms2_SpectralRedundancy.md) when consolidating mzML-derived summaries. The table is the launching point for MS2-first feature construction.

## Code
```python
SummMS2 = np.array([
    [300.1234, 245.6, 18240, 1.2e6, 0.34, 240.1, 248.3, 3, 7021],
    [450.2011, 512.3, 19305, 8.5e5, 0.42, 509.7, 516.8, 2, 7150]
])
```

## Key operations
- Downstream functions (`ms2_features_stats`, `feat_ms2_Gauss`) read `mz`, `RT`, and `MS2_Fullsignal_id` from columns 0–2.
- Columns 5–7 store chromatographic umbrellas (`min_RT`, `max_RT`, `N_spec`) used to transfer RT context to [`MS2_Features`](./MS2_Features.md) and [`AlignedSamplesDF`](./AlignedSamplesDF.md).
- Column 8 retains the representative MS2 spectrum ID for provenance when writing logs or exporting spectra.

## Parameters / columns
1. `mz_(Da)`: Gaussian centroid of the MS2 precursor.
2. `RT_(s)`: retention time of the MS2 event.
3. `MS2_Fullsignal_id`: scan index from the raw file.
4. `TotalInt_(a.u.)`: sum of intensities inside the MS2 spectrum.
5. `maxInt_frac`: ratio of the most intense fragment to the total intensity.
6. `min_RT_(s)`: minimum RT observed among redundant spectra.
7. `max_RT_(s)`: maximum RT among redundant spectra.
8. `N_ms2_spec`: number of redundant spectra merged.
9. `ms2_spec_id`: ID of the representative MS2 spectrum kept after clustering.

## Input
- [`AllMS2Data`](../Functions/AllMS2Data.md) builds this table directly from `DataSet`.
- [`ms2_SpectralRedundancy`](../Functions/ms2_SpectralRedundancy.md) re-generates `SummMS2` from spreadsheets.

## Output
- Consumed by [`ms2_features_stats`](../Functions/ms2_features_stats.md) for MS1 refinement.
- Fed into [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md) to build [`MS2_Features`](./MS2_Features.md).

## Functions
- [`AllMS2Data`](../Functions/AllMS2Data.md)
- [`ms2_SpectralRedundancy`](../Functions/ms2_SpectralRedundancy.md)
- [`ms2_features_stats`](../Functions/ms2_features_stats.md)
- [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md)

## Called by
- Workflow notebooks (`feat.-ms2-Gauss.ipynb`) when orchestrating MS2-first extraction.

## Example table

| mz_(Da) | RT_(s) | MS2_Fullsignal_id | TotalInt_(a.u.) | maxInt_frac | min_RT_(s) | max_RT_(s) | N_ms2_spec | ms2_spec_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 300.1234 | 245.6 | 18240 | 1.2e6 | 0.34 | 240.1 | 248.3 | 3 | 7021 |
| 450.2011 | 512.3 | 19305 | 8.5e5 | 0.42 | 509.7 | 516.8 | 2 | 7150 |

These columns define each MS2 umbrella’s mass accuracy and redundancy context.
