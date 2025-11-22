---
title: All_FeaturesTable
kind: table
source: Variables/All_FeaturesTable
last_updated: 2025-02-14
---

## Description
`All_FeaturesTable` is the vertical concatenation of per-sample `MS2_Features` exports. [`JoiningFeatures`](../Functions/JoiningFeatures.md) reads every feature spreadsheet inside a results folder, appends the sample index, and merges them into a single numpy array that still preserves the [`MS2_Features`](./MS2_Features.md) column order. This stacked table feeds the alignment stage.

## Code
```python
All_FeaturesTable = np.array([
    [18240, 10021, 245.6, 300.1234, 1.5e-03, 8.2e05, 0.997, 28,
     1.2e-04, 0.40, 299.118, 301.129, 240.1, 248.3, 3, 7021, 0],
    [18241, 10040, 247.0, 300.1236, 1.4e-03, 7.9e05, 0.993, 25,
     1.4e-04, 0.47, 299.119, 301.130, 241.0, 249.0, 2, 7025, 1]
])
```

## Key operations
- Created by [`JoiningFeatures`](../Functions/JoiningFeatures.md) after filtering by `mz_min/max` and `RT_min/max`.
- The last column (`sample_id`) tells [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md) which sample contributed each row.
- Intensities (column 5) and RTs (column 2) are copied into aligned matrices for their respective samples.

## Parameters / columns
Columns 0–15 mirror [`MS2_Features`](./MS2_Features.md). Column 16 is new:
- `sample_id`: zero-based index assigned by `JoiningFeatures`, also used to map onto column positions in alignment matrices.

## Input
- Built from per-sample feature spreadsheets stored under a results folder created by `feat_ms2_Gauss` or GA-based refinements.

## Output
- Consumed directly by [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md) and by cluster inspection notebooks.

## Functions
- [`JoiningFeatures`](../Functions/JoiningFeatures.md)
- [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md)

## Called by
- Batch alignment pipelines when generating experiment-wide matrices.

## Example table

| ms2_id | ms1_id | RT_(s) | mz_(Da) | mz_std_(Da) | I_total_(a.u.) | Gauss_r2 | CI_(ppm) | sample_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18240 | 10021 | 245.6 | 300.1234 | 0.0015 | 8.2e05 | 0.997 | 0.40 | 0 |
| 18241 | 10040 | 247.0 | 300.1236 | 0.0014 | 7.9e05 | 0.993 | 0.47 | 1 |

Only a subset of columns is shown; the actual array contains the full set from [`MS2_Features`](./MS2_Features.md).
