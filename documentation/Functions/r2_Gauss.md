---
title: r2_Gauss
kind: function
source: Functions/r2_Gauss.py
last_updated: 2025-02-14
---

## Description
Computes the coefficient of determination (r²) between observed chromatogram intensities and the Gaussian model returned by [`GaussianPeak`](./GaussianPeak.md). Used to assess fit quality in [`Normal_Fit`](./Normal_Fit.md).

## Code
```python
import numpy as np
from GaussianPeak import *
def r2_Gauss(PeakData,GaussianParameters):
    mz=GaussianParameters[0]
    mz_std=GaussianParameters[1]
    I_total=GaussianParameters[2]
    Gaussian_Int=GaussianPeak(PeakData[:,0],mz,mz_std,I_total)
    I_mean=np.mean(PeakData[:,1])
    SS_tot=np.sum((PeakData[:,1]-I_mean)**2)
    SS_res=np.sum((Gaussian_Int-PeakData[:,1])**2)
    r2=1-SS_res/SS_tot
    return [r2]
```

## Output
- List `[r²]` appended to fitted parameter lists.

## Called by
- [`Normal_Fit`](./Normal_Fit.md)

## Example
```python
r2 = r2_Gauss(PeakData, GaussianParameters)[0]
```
