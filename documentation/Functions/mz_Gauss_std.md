---
title: mz_Gauss_std
kind: function
source: Functions/mz_Gauss_std.py
last_updated: 2025-02-14
---

## Description
`mz_Gauss_std` estimates Gaussian parameters (centroid, standard deviation, intercept, r², total area) from raw peak data by performing a linear regression on log-intensity vs. squared deviation. Used by [`ms2Peak`](./ms2Peak.md) and [`mzPeak`](./mzPeak.md) to initialize Gaussian fits.

## Code
```python
from scipy import stats
import numpy as np
def mz_Gauss_std(PeakData,Points_for_regression=4):
    PeakData=PeakData[PeakData[:,1]>0,:].copy()
    maxInt=np.max(PeakData[:,1])
    maxInt_Loc=np.where(PeakData[:,1]==maxInt)[0][0]
    mz_maxInt=PeakData[maxInt_Loc,0]
    mz_DifVec=np.abs(PeakData[:,0]-mz_maxInt)
    PeakData=PeakData[mz_DifVec.argsort(),:]
    Closest_PeakData=PeakData[:Points_for_regression,:]
    log_Int_Vec=np.log(Closest_PeakData[:,1]/maxInt)
    Variance_mz_vec=(Closest_PeakData[:,0]-mz_maxInt)**2
    X=log_Int_Vec
    Y=Variance_mz_vec
    reg=stats.linregress(X,Y)
    m=reg[0]
    b=reg[1]
    r2=reg[2]**2
    mz_std=np.sqrt(-m/2)
    sqrt2pi=2.5066282746310002 #np.sqrt(np.pi*2)
    I_total=maxInt*mz_std*sqrt2pi
    GaussStats=[mz_maxInt,mz_std,b,r2,I_total]
    return GaussStats
```

## Key operations
- Selects the `Points_for_regression` closest points to the most intense fragment.
- Uses the Gaussian log-linear relationship to estimate variance.
- Returns both width and approximated total intensity for downstream fitting.

## Output
- `GaussStats = [mz_centroid, mz_std, intercept, r², I_total]`

## Called by
- [`ms2Peak`](./ms2Peak.md)
- [`mzPeak`](./mzPeak.md)

## Example
```python
stats = mz_Gauss_std(PeakData, Points_for_regression=5)
```
