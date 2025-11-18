---
title: mz_RT_spectrum_filter
kind: function
source: Functions/mz_RT_spectrum_filter.py
last_updated: 2025-02-14
---

## Description
`mz_RT_spectrum_filter` inspects a single spectrum object, verifies that it is MS2, falls within RT/m/z bounds, and appends its summary metrics to [`SummMS2`](../Variables/SummMS2.md). It is the per-spectrum worker used by [`AllMS2Data`](./AllMS2Data.md).

## Code
```python
import numpy as np
def mz_RT_spectrum_filter(SpectralSignals,SummMS2,min_RT,max_RT,min_mz,max_mz,spectrum_id):
    MSLevel=SpectralSignals.getMSLevel()
    if MSLevel!=2:
        return SummMS2
    RT=SpectralSignals.getRT()
    if RT<min_RT or RT>max_RT:
        return SummMS2
    Precursor=SpectralSignals.getPrecursors()[0]
    MZ=Precursor.getMZ()
    if MZ<min_mz or MZ>max_mz:
        return SummMS2
    Spectrum=np.array(SpectralSignals.get_peaks()).T
    maxInt=np.max(Spectrum[:,1])
    TotalInt=np.sum(Spectrum[:,1])
    AllInt=np.sum(Spectrum[:,1])
    maxInt_frac=maxInt/AllInt
    SummSpec=np.array([MZ,RT,spectrum_id,TotalInt,maxInt_frac])
    SummMS2.append(SummSpec)
    return SummMS2
```

## Key operations
- Rejects non-MS2 scans immediately, ensuring MS1 spectra never enter the MS2 summary.
- Applies rectangular RT/m/z filters using instrument metadata.
- Extracts peak arrays via `get_peaks()`, computes `TotalInt` and `maxInt_frac`, and appends them with the running `spectrum_id`.

## Parameters
- `SpectralSignals`: spectrum object from [`DataSet`](../Variables/DataSet.md).
- `SummMS2 (list)`: accumulator for MS2 summaries.
- `min_RT`, `max_RT` (seconds) and `min_mz`, `max_mz` (Da): bounds.
- `spectrum_id (int)`: index assigned while iterating through the raw file.

## Input
- Receives `SpectralSignals` and current `SummMS2` from [`AllMS2Data`](./AllMS2Data.md).

## Output
- Returns the updated list `SummMS2` (later converted to numpy array).

## Functions
- Uses numpy for intensity calculations.

## Called by
- [`AllMS2Data`](./AllMS2Data.md).

## Examples
```python
from Functions.mz_RT_spectrum_filter import mz_RT_spectrum_filter

class MockSpectrum:
    def __init__(self, level, rt, precursor_mz, peaks):
        self._level, self._rt, self._precursor_mz, self._peaks = level, rt, precursor_mz, peaks
    def getMSLevel(self):
        return self._level
    def getRT(self):
        return self._rt
    def getPrecursors(self):
        return [type('P', (), {'getMZ': lambda self: self})(self._precursor_mz)]
    def get_peaks(self):
        return self._peaks

summ = []
mock = MockSpectrum(2, 120.5, 300.12, [[300.12, 5e4], [301.0, 1e3]])
summ = mz_RT_spectrum_filter(mock, summ, 100, 200, 250, 400, spectrum_id=10)
print(summ[-1])  # [300.12, 120.5, 10, total_int, max_int_frac]
```
This example shows how a single spectrum is validated and summarized before aggregation.
