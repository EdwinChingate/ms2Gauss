---
title: mzPeak
kind: function
source: Functions/mzPeak.py
last_updated: 2025-02-14
---

## Description
`mzPeak` extracts an MS1 peak window from `DataSet` around a target m/z. It repeatedly calls `Find_mzPeak` to collect data and adjusts the Gaussian width using `mz_Gauss_std` until convergence. The output is consumed by [`ms2_features_stats`](./ms2_features_stats.md) and [`ms2_peak_stats`](./ms2_peak_stats.md).

## Code
```python
from Find_mzPeak import *
from mz_Gauss_std import *
def mzPeak(DataSet,spectrum_idVec,mz,mz_std=2e-3,stdDistance=3,count=0,MaxCount=3,Points_for_regression=5,minSignals=7,minInt=1e3):
    PeakData_and_meta=Find_mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=mz_std,stdDistance=stdDistance,MaxCount=MaxCount,minInt=minInt)
    if len(PeakData_and_meta)==0:
        return []
    PeakData=PeakData_and_meta[0]
    spectrum_id=PeakData_and_meta[1]
    GaussStats=mz_Gauss_std(PeakData,Points_for_regression=Points_for_regression)
    New_mz_std=GaussStats[1]
    if New_mz_std>mz_std and count<MaxCount:
        PeakData=mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=New_mz_std,count=count+1,minInt=minInt)[0]
    PeakData_and_Stats=[PeakData,GaussStats,spectrum_id]
    return PeakData_and_Stats
```

## Key operations
- Retrieves raw data from the closest MS1 scans using `spectrum_idVec`.
- Estimates Gaussian parameters via `mz_Gauss_std` and recursively widens the window if the new standard deviation exceeds the previous one.

## Parameters
- `DataSet`: MS1 iterable.
- `spectrum_idVec`: list of MS1 scan indices from [`closest_ms1_spec`](./closest_ms1_spec.md).
- `mz`, `mz_std`, `stdDistance`: extraction window.
- `MaxCount`: recursion limit for widening the window.
- `Points_for_regression`, `minSignals`, `minInt`: controls for Gaussian estimation.

## Output
- `[PeakData, GaussStats, spectrum_id]` where `PeakData` is an array of `[m/z, intensity]` and `GaussStats` contains initial Gaussian parameters.

## Called by
- [`ms2_features_stats`](./ms2_features_stats.md)
- [`ms2_peak_stats`](./ms2_peak_stats.md)

## Example
```python
peak_bundle = mzPeak(DataSet, spectrum_idVec=[10020,10021], mz=300.123)
```
