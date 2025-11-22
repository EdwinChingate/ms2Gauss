---
title: ms2_spectrum
kind: function
source: Functions/ms2_spectrum.py
last_updated: 2025-02-14
---

## Description
`ms2_spectrum` cleans a raw MS2 profile (`RawSpectrum`), iteratively fits Gaussian fragment peaks using [`ms2_peakStats_safe`](./ms2_peakStats_safe.md), and returns a sorted fragment table enriched with relative intensities. Scientifically, it enforces quality metrics (minimum signals, relative intensity coverage, Gaussian goodness-of-fit) so that only structurally interpretable fragments seed the MS2-first workflow.

**Math notes**  
Each fragment peak is estimated with Gaussian statistics (`mz`, `mz_std`, `Intensity`) and a quality score. After all peaks are extracted, the function appends relative intensity percentages: \(I_{\text{rel}} = 100 \times I_i / I_{\text{max}}\).

## Code
```python
import numpy as np
from ms2_peakStats_safe import *
def ms2_spectrum(RawSpectrum,DataSetName,ms_id,LogFileName,mz_std=2e-3,stdDistance=3,minQuality=100,minInt=1e2,minSignals=4,MaxCount=3,Points_for_regression=4,minPeaks=2,sort=2,as_des=-1):
    RawSpectrum=RawSpectrum[RawSpectrum[:,1]>0,:]
    TotalInt=sum(RawSpectrum[:,1])
    if len(RawSpectrum[:,0])<minSignals:
        return []
    Spectrum=[]
    while True:
        maxInt=np.max(RawSpectrum[:,1])
        if maxInt<minInt:
            break
        maxIntLoc=RawSpectrum[:,1]==maxInt
        mz_maxInt=RawSpectrum[maxIntLoc,0][0]
        peak_stats=ms2_peakStats_safe(RawSpectrum=RawSpectrum,DataSetName=DataSetName,ms_id=ms_id,mz=mz_maxInt,LogFileName=LogFileName,TotalInt=TotalInt,mz_std=mz_std,stdDistance=stdDistance,minSignals=minSignals,MaxCount=MaxCount,minInt=minInt,Points_for_regression=Points_for_regression)
        if len(peak_stats)>0:
            min_mz_peak=peak_stats[7]
            max_mz_peak=peak_stats[8]
            Spectrum.append(peak_stats)
        else:
            min_mz_peak=mz_maxInt-mz_std*stdDistance
            max_mz_peak=mz_maxInt+mz_std*stdDistance
        Latest_peakFilter=(RawSpectrum[:,0]<min_mz_peak)|(RawSpectrum[:,0]>max_mz_peak)
        RawSpectrum=RawSpectrum[Latest_peakFilter,:]
        if len(RawSpectrum[:,0])<minSignals:
            break
    if len(Spectrum)<minPeaks:
        return []
    Spectrum=np.array(Spectrum)
    Spectrum=Spectrum[(as_des*Spectrum[:,sort]).argsort(),:]
    RelIntVec=(Spectrum[:,2]/Spectrum[0,2]*100).reshape(-1, 1)
    Spectrum=np.hstack((Spectrum,RelIntVec))
    QualityFilter=Spectrum[:,6]<minQuality
    Spectrum=Spectrum[QualityFilter,:]
    return Spectrum
```

## Key operations
- Removes non-positive intensities to avoid log/ratio errors.
- Iteratively centers a Gaussian window around the highest remaining peak and calls [`ms2_peakStats_safe`](./ms2_peakStats_safe.md) for robust fitting/logging.
- Removes the processed m/z window from the working spectrum to prevent duplicate detections.
- Enforces a minimum number of peaks and sorts the fragment list by `sort` column (default intensity) and `as_des` ordering.
- Appends relative intensity percentages and filters by `minQuality` to keep reliable fragments.

## Parameters
- `RawSpectrum (np.ndarray)`: see [`RawSpectrum`](../Variables/RawSpectrum.md).
- `DataSetName (str)`, `ms_id (int)`, `LogFileName (str)`: identifiers for logging exceptions.
- `mz_std (float)`, `stdDistance (float)`: Gaussian width and integration span.
- `minQuality (float)`: threshold on the quality metric returned by `ms2_peakStats_safe` (lower is better in this implementation).
- `minInt (float)`, `minSignals (int)`: intensity and point-count filters before fitting.
- `MaxCount`, `Points_for_regression`: control polynomial regression or peak-shape estimation inside helper functions.
- `minPeaks (int)`: ensures at least two fragments remain, enabling cosine similarity downstream.
- `sort (int)`, `as_des (±1)`: determine sorting column and ascending/descending order.

## Input
- [`RawSpectrum`](../Variables/RawSpectrum.md)
- Metadata strings used for logging.

## Output
- numpy array of fragment statistics including relative intensity (%). Each row originates from [`ms2_peakStats_safe`](./ms2_peakStats_safe.md).

## Functions
- [`ms2_peakStats_safe`](./ms2_peakStats_safe.md)

## Called by
- Higher-level MS2 processing pipelines before redundancy clustering or fragment export.

## Examples
```python
import numpy as np
import matplotlib.pyplot as plt
from Functions.ms2_spectrum import ms2_spectrum

raw = np.array([
    [150.0234, 1.2e4],
    [150.0240, 5.2e4],
    [200.1111, 7.1e4],
    [200.1120, 8.3e4],
    [250.0500, 2.0e4]
])
# Mock ms2_peakStats_safe by patching if necessary during testing
spectrum = ms2_spectrum(raw, 'Sample_A', ms_id=42, LogFileName='ms2.log', minInt=5e3, minSignals=3, minPeaks=1)
if len(spectrum) > 0:
    plt.bar(np.arange(spectrum.shape[0]), spectrum[:,2])
    plt.xlabel('Fragment index')
    plt.ylabel('Intensity (a.u.)')
    plt.title('Accepted fragments after ms2_spectrum')
    plt.show()
```
When `ms2_peakStats_safe` is available, this code plots the intensities of the surviving fragments.
