---
title: AlignedSamples_RT_DF
kind: table
source: Variables/AlignedSamples_RT_DF
last_updated: 2025-02-14
---

## Description
`AlignedSamples_RT_DF` mirrors [`AlignedSamplesDF`](./AlignedSamplesDF.md) but replaces per-sample intensity columns with the retention times observed in each sample. It is returned as the second element of [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md) to help diagnose chromatographic drifts.

## Code
```python
Columns = ['mz_(Da)','mz_std_(Da)','mz_CI_(Da)','mz_CI_(ppm)',
           'RT_(s)','min_RT_(s)','max_RT_(s)','Sample_A','Sample_B']
AlignedSamples_RT_DF = pd.DataFrame([
    [300.12345, 1.4e-03, 1.1e-04, 0.37, 245.6, 240.1, 248.3, 245.4, 246.0]
], columns=Columns)
```

## Key operations
- Shares metadata columns (0–6) with `AlignedSamplesDF`.
- Sample columns store RTs pulled from [`All_FeaturesTable`](./All_FeaturesTable.md) column 2 during alignment.
- Enables visualization of chromatographic shifts or umbrella violations without recomputing intensities.

## Parameters / columns
- Same interpretation as `AlignedSamplesDF`, except sample columns contain RT (seconds) instead of intensity.

## Input
- Created in lockstep with `AlignedSamplesDF` within [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md).

## Output
- Optionally exported as `RT_<timestamp>.xlsx` for quality-control notebooks.

## Functions
- [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md)

## Called by
- Alignment QC routines and chromatographic drift assessments.

## Example table

| mz_(Da) | RT_(s) | min_RT_(s) | max_RT_(s) | Sample_A (RT) | Sample_B (RT) |
| --- | --- | --- | --- | --- | --- |
| 300.12345 | 245.6 | 240.1 | 248.3 | 245.4 | 246.0 |

The per-sample RT columns help verify that each detection falls inside the umbrella bounds.
