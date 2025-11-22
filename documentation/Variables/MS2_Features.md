---
title: MS2_Features
kind: table
source: Variables/MS2_Features
last_updated: 2025-02-14
---

## Description
`MS2_Features` is the Gaussian-refined feature catalog returned by [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md). Each row ties an MS2 event to its MS1-derived centroid, uncertainty, and chromatographic umbrella. The table feeds downstream alignment (`Features_ms2_SamplesAligment`) and filtering routines.

## Code
```python
MS2_Features = np.array([
    [18240, 10021, 245.6, 300.123401, 1.5e-03, 8.2e05, 0.997, 28,
     1.2e-04, 0.40, 299.118, 301.129, 240.1, 248.3, 3, 7021]
])
```

## Key operations
- Columns 0–1 trace provenance: MS2 scan ID and the selected MS1 scan ID.
- Columns 3–6 hold Gaussian fit results (m/z, standard deviation, integrated intensity, r²) computed by [`ms2_features_stats`](../Functions/ms2_features_stats.md).
- Columns 8–9 provide absolute and ppm confidence intervals derived from Student’s t-statistic.
- Columns 12–15 carry chromatographic umbrella metadata inherited from [`SummMS2`](./SummMS2.md).

## Parameters / columns
1. `ms2_id`: raw MS2 scan index (`MS2_Fullsignal_id`).
2. `ms1_id`: MS1 scan chosen via [`closest_ms1_spec`](../Functions/closest_ms1_spec.md).
3. `RT_(s)`: RT of the MS2 detection.
4. `mz_(Da)`: Gaussian centroid fitted from MS1 data.
5. `mz_std_(Da)`: Gaussian standard deviation.
6. `I_total_(a.u.)`: integrated intensity of the Gaussian.
7. `Gauss_r2`: coefficient of determination between the model and observed MS1 peak.
8. `N_points`: number of MS1 data points used in the fit.
9. `CI_(Da)`: confidence interval on m/z in Daltons.
10. `CI_(ppm)`: same interval expressed in ppm.
11. `min_mz_(Da)`: lower bound of the integration window.
12. `max_mz_(Da)`: upper bound of the integration window.
13. `min_RT_(s)`: start of the chromatographic umbrella.
14. `max_RT_(s)`: end of the umbrella.
15. `N_ms2_spec`: number of MS2 spectra merged for this feature.
16. `spectra_id`: representative MS2 spectrum ID preserved during redundancy removal.

## Input
- Produced by [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md).

## Output
- Consumed by [`Cluster_ms2_Features`](../Functions/Cluster_ms2_Features.md) and [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md).

## Functions
- [`ms2_features_stats`](../Functions/ms2_features_stats.md) populates most columns.
- [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md) appends umbrella metadata.
- [`Cluster_ms2_Features`](../Functions/Cluster_ms2_Features.md) converts this array into a pandas DataFrame when clustering is required.

## Called by
- Workflow notebooks, alignment modules, and downstream filtering functions (e.g., `Samples_NFeatures_Filter`).

## Example table

| ms2_id | ms1_id | RT_(s) | mz_(Da) | mz_std_(Da) | I_total_(a.u.) | Gauss_r2 | N_points | CI_(Da) | CI_(ppm) | min_RT_(s) | max_RT_(s) | N_ms2_spec |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18240 | 10021 | 245.6 | 300.123401 | 0.0015 | 8.2e05 | 0.997 | 28 | 1.2e-04 | 0.40 | 240.1 | 248.3 | 3 |

Additional columns (`min_mz_(Da)`, `max_mz_(Da)`, `spectra_id`) are omitted here for brevity but present in the actual array.
