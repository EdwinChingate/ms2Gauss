---
title: ms2Peak
kind: function
source: Functions/ms2Peak.py
last_updated: 2025-02-14
---

## Description
`ms2Peak` extracts a local fragment window from `RawSpectrum`, optionally widening the window until enough points are available, and returns both the raw data and preliminary Gaussian statistics computed by [`mz_Gauss_std`](./mz_Gauss_std.md). It is used by [`ms2_peak_stats`](./ms2_peak_stats.md) to seed Gaussian fitting.

## Code
```python
from Find_ms2Peak import *
from mz_Gauss_std import *
def ms2Peak(RawSpectrum,mz,mz_std=2e-3,stdDistance=3,minSignals=4,count=0,MaxCount=3,minInt=1e3,Points_for_regression=4):
    PeakData=Find_ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=mz_std,stdDistance=stdDistance,minSignals=minSignals,MaxCount=MaxCount,minInt=minInt)
    if len(PeakData)==0:
        return []
    GaussStats=mz_Gauss_std(PeakData,Points_for_regression=Points_for_regression)
    New_mz_std=GaussStats[1]
    if New_mz_std>mz_std and count<MaxCount:
        PeakData=ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=New_mz_std,stdDistance=stdDistance,minSignals=minSignals,count=count+1,MaxCount=MaxCount,minInt=minInt,Points_for_regression=Points_for_regression)[0]
    PeakData_and_Stats=[PeakData,GaussStats]
    return PeakData_and_Stats
```

## Key operations
- Calls [`Find_ms2Peak`](./Find_ms2Peak.md) to select data within ±`stdDistance * mz_std`.
- Fits an initial Gaussian via [`mz_Gauss_std`](./mz_Gauss_std.md) and recursively widens the window if the estimated width grows.

## Parameters
- `RawSpectrum`: MS2 array.
- `mz`, `mz_std`, `stdDistance`: initial window definition.
- `minSignals`: minimum number of data points required.
- `MaxCount`: recursion limit for widening.
- `Points_for_regression`: number of points used when estimating Gaussian variance.
- `minInt`: minimum intensity filter.

## Output
- `[PeakData, GaussStats]` where `PeakData` contains `[m/z, intensity]` samples and `GaussStats` includes centroid, std, intercept, r², and approximate area.

## Called by
- [`ms2_peak_stats`](./ms2_peak_stats.md)

## Example
```python
peak_data, gauss_stats = ms2Peak(RawSpectrum, mz=150.02)
```
