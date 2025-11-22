---
title: WriteLog
kind: function
source: Functions/WriteLog.py
last_updated: 2025-02-14
---

## Description
`WriteLog` records failed MS2 peak fits. It estimates the relative contribution of the targeted peak to the total spectrum, formats diagnostic parameters, and appends the entry to `LogFileName`. This information helps troubleshoot `ms2_peak_stats` failures.

## Code
```python
from ms2Peak_contribution import *
from Parameters_to_string import *
def WriteLog(RawSpectrum,Parameters,TotalInt,LogFileName='LogMS2_peaks.csv'):
    mz=Parameters[2]
    mz_std=Parameters[3]
    stdDistance=Parameters[4]
    relative_contribution=ms2Peak_contribution(RawSpectrum=RawSpectrum,TotalInt=TotalInt,mz=mz,mz_std=mz_std,stdDistance=stdDistance)
    Parameters=relative_contribution+Parameters
    toWrite=Parameters_to_string(Parameters)
    LogFile=open(LogFileName,'a')
    LogFile.write(toWrite)
    LogFile.close()
```

## Key operations
- Calls `ms2Peak_contribution` to quantify how much of the spectrum falls within the Gaussian window.
- Uses `Parameters_to_string` to serialize the metadata into CSV-friendly text.
- Appends to the log file without overwriting previous entries.

## Parameters
- `RawSpectrum`: raw MS2 data.
- `Parameters`: list passed from [`ms2_peakStats_safe`](./ms2_peakStats_safe.md), typically `[DataSetName, ms_id, mz, ...]`.
- `TotalInt`: sum of intensities for normalization.
- `LogFileName`: path of the log file.

## Output
- None (side effect: file append).

## Called by
- [`ms2_peakStats_safe`](./ms2_peakStats_safe.md)

## Example
```python
WriteLog(RawSpectrum, Parameters=['Sample', 10, 150.02, 2e-3, 3], TotalInt=RawSpectrum[:,1].sum())
```
