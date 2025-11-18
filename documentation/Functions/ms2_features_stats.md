---
title: ms2_features_stats
kind: function
source: Functions/ms2_features_stats.py
last_updated: 2025-02-14
---

## Description
`ms2_features_stats` links an MS2 detection from [`SummMS2`](../Variables/SummMS2.md) to the nearest MS1 spectra stored in [`MS1IDVec`](../Variables/MS1IDVec.md), extracts the MS1 peak via `mzPeak`, fits a Gaussian using [`Normal_Fit`](./Normal_Fit.md), and computes confidence intervals on the precursor m/z. The output row forms the backbone of [`MS2_Features`](../Variables/MS2_Features.md).

**Math notes**  
Given \(N\) MS1 data points and fitted standard deviation \(\sigma\), the function propagates uncertainty via Student’s t:
\[
\text{CI}_{\text{Da}} = t_{1-\alpha, N-1} \frac{\sigma}{\sqrt{N}}, \qquad
\text{CI}_{\text{ppm}} = 10^6 \frac{\text{CI}_{\text{Da}}}{m/z}
\]
This captures instrument resolving power and sampling density.

## Code
```python
from scipy import stats
from mzPeak import *
from closest_ms1_spec import *
from Normal_Fit import *
def ms2_features_stats(DataSet,MS2_id,SummMS2,MS1IDVec,mz_std=2e-3,MS2_to_MS1_ratio=10,stdDistance=3,MaxCount=3,Points_for_regression=5,minSignals=7,alpha=0.01):
    RT=SummMS2[MS2_id,1]
    mz=SummMS2[MS2_id,0]
    MS2_Fullsignal_id=SummMS2[MS2_id,2]
    spectrum_idVec=closest_ms1_spec(mz=mz,RT=RT,MS2_Fullsignal_id=MS2_Fullsignal_id,SummMS2=SummMS2,MS1IDVec=MS1IDVec,MS2_to_MS1_ratio=MS2_to_MS1_ratio)
    PeakData_and_Stats=mzPeak(DataSet=DataSet,spectrum_idVec=spectrum_idVec,mz=mz,mz_std=mz_std,stdDistance=stdDistance,MaxCount=MaxCount,Points_for_regression=Points_for_regression,minSignals=minSignals)
    if len(PeakData_and_Stats)==0:
        return []
    spectrum_id=[int(PeakData_and_Stats[2])]
    NormalParameters=Normal_Fit(PeakData_and_Stats=PeakData_and_Stats)
    Nsignals=len(PeakData_and_Stats[0][:,0])
    mz=NormalParameters[0]
    mz_std=NormalParameters[1]
    min_mz=[mz-stdDistance*mz_std]
    max_mz=[mz+stdDistance*mz_std]
    tref=stats.t.interval(1-alpha, Nsignals-1)[1]
    ConfidenceIntervalDa=[tref*mz_std/np.sqrt(Nsignals)]
    ConfidenceInterval=[tref*mz_std/np.sqrt(Nsignals)/mz*1e6]
    features_stats=[int(MS2_Fullsignal_id)]+spectrum_id+[RT]+NormalParameters+[Nsignals]+ConfidenceIntervalDa+ConfidenceInterval+min_mz+max_mz
    return features_stats
```

## Key operations
- Retrieves MS2 metadata (`mz`, `RT`, `MS2_Fullsignal_id`).
- Uses [`closest_ms1_spec`](./closest_ms1_spec.md) to find MS1 scan IDs preceding the MS2 event.
- Calls `mzPeak` to extract MS1 peak data centered on the MS2 m/z.
- Fits a Gaussian via [`Normal_Fit`](./Normal_Fit.md) to obtain refined `mz`, `mz_std`, and `I_total` along with `r²`.
- Calculates confidence intervals and integration bounds, packaging them into a single list.

## Parameters
- `DataSet`: see [`DataSet`](../Variables/DataSet.md).
- `MS2_id (int)`: row index inside [`SummMS2`](../Variables/SummMS2.md).
- `SummMS2`: MS2 summary table.
- `MS1IDVec`: MS1 scan mapping.
- `mz_std`, `stdDistance`: initial Gaussian window for MS1 extraction.
- `MS2_to_MS1_ratio`: number of MS1 scans inspected relative to the MS2 scan index.
- `MaxCount`, `Points_for_regression`, `minSignals`: controls for `mzPeak`.
- `alpha`: significance level for the t-interval.

## Input
- [`DataSet`](../Variables/DataSet.md)
- [`SummMS2`](../Variables/SummMS2.md)
- [`MS1IDVec`](../Variables/MS1IDVec.md)

## Output
- List containing `[ms2_id, ms1_id, RT, mz, mz_std, I_total, r², N_points, CI_Da, CI_ppm, min_mz, max_mz]`.

## Functions
- [`closest_ms1_spec`](./closest_ms1_spec.md)
- [`mzPeak`](./mzPeak.md)
- [`Normal_Fit`](./Normal_Fit.md)
- `scipy.stats.t.interval`

## Called by
- [`feat_ms2_Gauss`](./feat_ms2_Gauss.md)

## Examples
```python
import numpy as np
from Functions.ms2_features_stats import ms2_features_stats

# Mock datasets: replace with actual loaders in production
DataSet = [...]  # iterable of MS1 spectra
SummMS2 = np.array([[300.123, 245.6, 18240, 1.2e6, 0.34, 240.1, 248.3, 3, 7021]])
MS1IDVec = np.array([[18000, 245.2], [18005, 245.5], [18010, 245.8]])

feature = ms2_features_stats(DataSet=DataSet, MS2_id=0, SummMS2=SummMS2,
                             MS1IDVec=MS1IDVec, minSignals=5, alpha=0.01)
```
To visualize confidence intervals (mock data):
```python
import matplotlib.pyplot as plt
mz = feature[3]
ci_ppm = feature[9]
plt.errorbar([0], [mz], yerr=[[ci_ppm],[ci_ppm]], fmt='o')
plt.ylabel('m/z (Da)')
plt.title('MS2 feature confidence interval (ppm scaled)')
plt.show()
```
