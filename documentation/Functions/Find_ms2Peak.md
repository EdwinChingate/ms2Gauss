---
title: Find_ms2Peak
kind: function
source: Functions/Find_ms2Peak.py
last_updated: 2025-02-14
---

## Description
Slices a raw MS2 spectrum around a target m/z, expanding the window if too few points are found. Provides the raw data used by [`ms2Peak`](./ms2Peak.md).

## Code
```python
import numpy as np
def Find_ms2Peak(RawSpectrum,mz,mz_std=2e-3,stdDistance=3,minSignals=4,count=0,MaxCount=3,minInt=1e3,RelativeContribution=False):
    if count==MaxCount:
        return []
    min_mz_peak=mz-mz_std*stdDistance
    max_mz_peak=mz+mz_std*stdDistance
    peakFilter=(RawSpectrum[:,0]>min_mz_peak)&(RawSpectrum[:,0]<max_mz_peak)&(RawSpectrum[:,1]>0)
    PeakData=RawSpectrum[peakFilter,:]
    if RelativeContribution:
        PeakInt=sum(PeakData[:,1])
        TotalInt=sum(RawSpectrum[:,1])
        relative_contribution=[int(PeakInt/TotalInt*100)]
    if (len(PeakData[:,0])<minSignals) and (count<MaxCount):
        PeakData=Find_ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=mz_std,stdDistance=stdDistance+1,count=count+1,minInt=minInt,minSignals=minSignals)
    return PeakData
```

## Parameters
- `RawSpectrum`: MS2 array.
- `mz`, `mz_std`, `stdDistance`: window definition.
- `minSignals`, `MaxCount`: control recursion when few points are present.
- `RelativeContribution (bool)`: optional flag to compute peak contribution.

## Output
- `PeakData`: filtered subset of the spectrum.

## Called by
- [`ms2Peak`](./ms2Peak.md)

## Example
```python
window = Find_ms2Peak(RawSpectrum, mz=150.02)
```
