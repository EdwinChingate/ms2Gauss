---
title: MS1IDVec
kind: table
source: Variables/MS1IDVec
last_updated: 2025-02-14
---

## Description
`MS1IDVec` maps MS1 scan indices to their retention times. It ensures MS2 detections can pull the correct MS1 chromatographic windows for Gaussian fitting. Each row is `[MS1_scan_id, RT_(s)]` and optionally includes additional metadata (e.g., TIC) appended by helper functions. Without this mapping, [`closest_ms1_spec`](../Functions/closest_ms1_spec.md) could not locate nearby MS1 scans for [`ms2_features_stats`](../Functions/ms2_features_stats.md).

## Code
```python
MS1IDVec = np.array([
    [10020, 244.8],
    [10021, 245.1],
    [10022, 245.4]
])
```

## Key operations
- Filtered by scan index and RT to ensure only MS1 events preceding a given MS2 scan are considered.
- Enables RT proximity calculations via `RT - MS1IDVec[:,1]` inside [`closest_ms1_spec`](../Functions/closest_ms1_spec.md).
- Serves as the backbone for chromatogram reconstruction in functions like `RetrieveChromatogram` (not yet documented).

## Parameters / columns
1. `MS1_scan_id`: integer index referencing `DataSet`.
2. `RT_(s)`: chromatographic time of the MS1 scan.

## Input
- Produced by helper functions such as `MS_L_IDs` when parsing Thermo RAW files.

## Output
- Consumed by [`ms2_features_stats`](../Functions/ms2_features_stats.md), [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md), and chromatographic refinement utilities.

## Functions
- [`closest_ms1_spec`](../Functions/closest_ms1_spec.md)
- [`ms2_features_stats`](../Functions/ms2_features_stats.md)
- [`feat_ms2_Gauss`](../Functions/feat_ms2_Gauss.md)

## Called by
- Notebook pipelines and chromatogram modules needing MS1 scan context.

## Example table

| MS1_scan_id | RT_(s) |
| --- | --- |
| 10020 | 244.8 |
| 10021 | 245.1 |
| 10022 | 245.4 |

This vector ensures MS2 events can anchor themselves to nearby MS1 scans.
