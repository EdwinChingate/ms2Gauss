---
title: AllMS2Data
kind: function
source: Functions/AllMS2Data.py
last_updated: 2025-02-14
---

## Description
`AllMS2Data` streams every spectrum in a `DataSet`, keeps only MS2 scans that fall within user-defined m/z and RT windows, and summarizes them into [`SummMS2`](../Variables/SummMS2.md). Each accepted spectrum is routed through [`mz_RT_spectrum_filter`](./mz_RT_spectrum_filter.md), which reports precursor m/z, RT, total intensity, and diagnostic ratios. The resulting array is sorted by m/z to support reproducible downstream clustering.

**Math notes**  
Filtering occurs in two dimensions: RT is constrained by `min_RT ≤ RT ≤ max_RT`, while m/z is constrained by `min_mz ≤ precursor_mz ≤ max_mz`. Summed intensities provide the total ion current for each spectrum, and `maxInt_frac = I_{\text{max}} / \sum I` offers a quick check on spectral concentration.

## Code
```python
import numpy as np
from mz_RT_spectrum_filter import *
def AllMS2Data(DataSet,min_RT=0,max_RT=1e5,min_mz=0,max_mz=1e4):
    SummMS2=[]
    FirstSpec=True
    spectrum_id=0
    for SpectralSignals in DataSet:
        SummMS2=mz_RT_spectrum_filter(SpectralSignals=SpectralSignals,SummMS2=SummMS2,min_RT=min_RT,max_RT=max_RT,min_mz=min_mz,max_mz=max_mz,spectrum_id=spectrum_id)
        spectrum_id+=1
    SummMS2=np.array(SummMS2)
    SummMS2=SummMS2[SummMS2[:,0].argsort(),:]
    return SummMS2
```

## Key operations
- Iterates once over `DataSet`, so memory footprint stays low even for large RAW files.
- Delegates RT/mz filtering to [`mz_RT_spectrum_filter`](./mz_RT_spectrum_filter.md), which inspects MS level and precursor metadata.
- Converts the Python list into a numpy array and sorts by `SummMS2[:,0]` (precursor m/z) for deterministic downstream behavior.

## Parameters
- `DataSet (iterable)`: Source of spectra, see [`DataSet`](../Variables/DataSet.md).
- `min_RT`, `max_RT` (float, seconds): Retention-time bounds for accepted MS2 events.
- `min_mz`, `max_mz` (float, Da): Mass bounds used to focus on relevant precursors.

## Input
- [`DataSet`](../Variables/DataSet.md): provides `SpectralSignals` objects.

## Output
- [`SummMS2`](../Variables/SummMS2.md): redundancy-aware MS2 summary table ready for MS2-first modeling.

## Functions
- [`mz_RT_spectrum_filter`](./mz_RT_spectrum_filter.md): inspects and appends eligible MS2 spectra.

## Called by
- Workflow notebooks (e.g., `feat.-ms2-Gauss.ipynb`) before executing [`ms2_spectrum`](./ms2_spectrum.md) or [`ms2_SpectralRedundancy`](./ms2_SpectralRedundancy.md).

## Examples
```python
import numpy as np
import matplotlib.pyplot as plt
from Functions.AllMS2Data import AllMS2Data

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

spectra = [
    MockSpectrum(2, 120.5, 300.12, [[300.12, 5e4], [310.00, 1e3]]),
    MockSpectrum(1, 120.7, None, [[300.10, 1e5]]),
    MockSpectrum(2, 500.0, 450.20, [[450.20, 8e4], [460.0, 5e3]])
]
SummMS2 = AllMS2Data(spectra, min_RT=100, max_RT=600, min_mz=250, max_mz=500)

plt.scatter(SummMS2[:,1], SummMS2[:,0], s=50)
plt.xlabel('RT (s)')
plt.ylabel('Precursor m/z (Da)')
plt.title('Accepted MS2 events')
plt.show()
```
The scatter plot reveals which precursors passed the RT/m/z filters.
