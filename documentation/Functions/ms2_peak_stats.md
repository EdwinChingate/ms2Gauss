---
title: ms2_peak_stats
kind: function
source: Functions/ms2_peak_stats.py
last_updated: 2025-02-14
---

## Description
`ms2_peak_stats` extracts a fragment-specific window from a raw MS2 spectrum via [`ms2Peak`](./ms2Peak.md), refines it with [`Normal_Fit`](./Normal_Fit.md), and calculates confidence intervals. It is the core analytical routine wrapped by [`ms2_peakStats_safe`](./ms2_peakStats_safe.md).

## Code
```python
from scipy import stats
from ms2Peak import *
from Normal_Fit import *
def ms2_peak_stats(RawSpectrum,mz,mz_std=2e-3,stdDistance=3,minSignals=5,MaxCount=3,minInt=1e3,Points_for_regression=4,alpha=0.01):
    PeakData_and_Stats=ms2Peak(RawSpectrum=RawSpectrum,mz=mz,mz_std=mz_std,stdDistance=stdDistance,minSignals=minSignals,MaxCount=MaxCount,minInt=minInt,Points_for_regression=Points_for_regression)
    if len(PeakData_and_Stats)==0:
        return []
    NormalParameters=Normal_Fit(PeakData_and_Stats=PeakData_and_Stats)
    Nsignals=len(PeakData_and_Stats[0][:,0])
    PeakData=PeakData_and_Stats[0]
    mz=NormalParameters[0]
    mz_std=NormalParameters[1]
    min_mz=[np.min(PeakData[:,0])]
    max_mz=[np.max(PeakData[:,0])]
    tref=stats.t.interval(1-alpha, Nsignals-1)[1]
    ConfidenceIntervalDa=[tref*mz_std/np.sqrt(Nsignals)]
    ConfidenceInterval=[tref*mz_std/np.sqrt(Nsignals)/mz*1e6]
    peak_stats=NormalParameters+[Nsignals]+ConfidenceIntervalDa+ConfidenceInterval+min_mz+max_mz
    return peak_stats
```

## Key operations
- Calls [`ms2Peak`](./ms2Peak.md) to collect intensity/RT data around `mz`.
- Fits a Gaussian with [`Normal_Fit`](./Normal_Fit.md).
- Computes confidence intervals exactly like [`ms2_features_stats`](./ms2_features_stats.md).

## Parameters
- `RawSpectrum`: MS2 array.
- `mz`, `mz_std`, `stdDistance`: define the window.
- `minSignals`, `MaxCount`, `minInt`, `Points_for_regression`, `alpha`: quality controls and confidence settings.

## Output
- List `[mz, mz_std, I_total, r², Nsignals, CI_Da, CI_ppm, min_mz, max_mz]`.

## Called by
- [`ms2_peakStats_safe`](./ms2_peakStats_safe.md)

## Example
```python
peak_stats = ms2_peak_stats(RawSpectrum, mz=150.02, minSignals=5)
```
