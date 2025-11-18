---
title: ms2_peakStats_safe
kind: function
source: Functions/ms2_peakStats_safe.py
last_updated: 2025-02-14
---

## Description
`ms2_peakStats_safe` wraps [`ms2_peak_stats`](./ms2_peak_stats.md) with exception handling and logging. When a Gaussian fit fails (e.g., insufficient points or singular matrices), it records the offending spectrum in `LogFileName` via [`WriteLog`](./WriteLog.md) and returns an empty list, allowing [`ms2_spectrum`](./ms2_spectrum.md) to skip the problematic window without crashing.

## Code
```python
from ms2_peak_stats import *
from WriteLog import *
def ms2_peakStats_safe(RawSpectrum,DataSetName,ms_id,mz,TotalInt,LogFileName,mz_std=2e-3,stdDistance=3,minSignals=5,MaxCount=3,minInt=1e3,Points_for_regression=4,alpha=0.01):
    while True:
        try:
            peak_stats=ms2_peak_stats(RawSpectrum=RawSpectrum,mz=mz,mz_std=mz_std,stdDistance=stdDistance,minSignals=minSignals,MaxCount=MaxCount,minInt=minInt,Points_for_regression=Points_for_regression)
            return peak_stats
        except:
            Parameters=[DataSetName,ms_id,mz,mz_std,stdDistance,minSignals,MaxCount,minInt,Points_for_regression,alpha]
            WriteLog(RawSpectrum=RawSpectrum,Parameters=Parameters,TotalInt=TotalInt,LogFileName=LogFileName)
            return []
```

## Key operations
- Repeats the call to [`ms2_peak_stats`](./ms2_peak_stats.md) once; on any exception it writes a diagnostic entry and exits.
- Captures important context (dataset, scan ID, target m/z, thresholds) and stores it alongside the raw spectrum for future debugging.
- Returns either the fitted peak stats (length ≥ 9 array) or an empty list so callers can decide how to proceed.

## Parameters
- `RawSpectrum`: see [`RawSpectrum`](../Variables/RawSpectrum.md).
- `DataSetName`, `ms_id`: identifiers included in the log entry.
- `mz`, `mz_std`, `stdDistance`: Gaussian window definitions.
- `minSignals`, `MaxCount`, `minInt`, `Points_for_regression`, `alpha`: fitting controls forwarded to `ms2_peak_stats` or recorded in the log.
- `TotalInt`: used by [`WriteLog`](./WriteLog.md) to assess spectrum quality.
- `LogFileName`: CSV/Excel file collecting failed fits.

## Input
- Called from [`ms2_spectrum`](./ms2_spectrum.md) with the current `RawSpectrum` slice.

## Output
- Either the result of [`ms2_peak_stats`](./ms2_peak_stats.md) or `[]` (failure).

## Functions
- [`ms2_peak_stats`](./ms2_peak_stats.md)
- [`WriteLog`](./WriteLog.md)

## Called by
- [`ms2_spectrum`](./ms2_spectrum.md)

## Examples
```python
from Functions.ms2_peakStats_safe import ms2_peakStats_safe
import numpy as np

raw = np.array([[150.0, 1e4], [150.01, 8e3], [150.02, 3e3]])
peak = ms2_peakStats_safe(raw, 'Sample_A', ms_id=10, mz=150.01,
                          LogFileName='ms2.log', TotalInt=raw[:,1].sum(),
                          minSignals=3, minInt=1e3)
if len(peak) == 0:
    print('Fit failed, check ms2.log for details')
else:
    print('Peak center:', peak[0])
```
This snippet demonstrates how the wrapper prevents the caller from crashing when `ms2_peak_stats` raises an exception.
