---
title: AlignedSamplesDF
kind: table
source: Variables/AlignedSamplesDF
last_updated: 2025-02-14
---

## Description
`AlignedSamplesDF` is the pandas DataFrame produced by [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md). Rows correspond to aligned MS2-derived features, while columns contain umbrella metadata plus one intensity column per sample. It facilitates cross-sample comparisons and downstream filtering.

## Code
```python
Columns = ['mz_(Da)','mz_std_(Da)','mz_CI_(Da)','mz_CI_(ppm)',
           'RT_(s)','min_RT_(s)','max_RT_(s)','Sample_A','Sample_B']
AlignedSamplesDF = pd.DataFrame([
    [300.12345, 1.4e-03, 1.1e-04, 0.37, 245.6, 240.1, 248.3, 8.2e05, 7.9e05]
], columns=Columns)
```

## Key operations
- Columns 0–6 summarize the consensus Gaussian parameters across samples.
- Sample columns (`Sample_A`, `Sample_B`, …) store per-sample intensities pulled from [`All_FeaturesTable`](./All_FeaturesTable.md).
- Retention-time umbrellas (`min_RT`, `max_RT`) guide chromatographic comparisons and blank filtering.

## Parameters / columns
1. `mz_(Da)`, `mz_std_(Da)`: averaged precursor centroid and width.
2. `mz_CI_(Da)`, `mz_CI_(ppm)`: averaged uncertainties.
3. `RT_(s)`: average RT across contributing samples.
4. `min_RT_(s)`, `max_RT_(s)`: umbrella bounds inherited from per-sample entries.
5. `Sample_*` columns: intensities for each aligned sample.

## Input
- Created from [`All_FeaturesTable`](./All_FeaturesTable.md) after clustering modules returned by [`ms2_SpectralSimilarityClustering`](../Functions/ms2_SpectralSimilarityClustering.md).

## Output
- Exported to Excel when `saveAlignedTable=True`.
- Serves as the canonical aligned matrix for downstream statistics (blank subtraction, treatment comparisons, etc.).

## Functions
- [`Features_ms2_SamplesAligment`](../Functions/Features_ms2_SamplesAligment.md)

## Called by
- Experimental filters (e.g., `Samples_AttributesFilter`) and visualization notebooks.

## Example table

| mz_(Da) | mz_std_(Da) | mz_CI_(ppm) | RT_(s) | min_RT_(s) | max_RT_(s) | Sample_A | Sample_B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 300.12345 | 0.0014 | 0.37 | 245.6 | 240.1 | 248.3 | 8.2e05 | 7.9e05 |

This layout allows quick inspection of feature intensities across multiple samples while retaining umbrella metadata.
