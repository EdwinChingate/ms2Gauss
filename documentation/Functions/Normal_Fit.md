---
title: Normal_Fit
kind: function
source: Functions/Normal_Fit.py
last_updated: 2025-02-14
---

## Description
`Normal_Fit` performs a nonlinear least-squares fit of the Gaussian model (`GaussianPeak`) to MS1 peak windows extracted by `mzPeak`. It returns the optimized centroid, width, intensity, and r² goodness-of-fit, enabling [`ms2_features_stats`](./ms2_features_stats.md) to quantify precursor precision.

## Code
```python
from scipy.optimize import curve_fit
from GaussianPeak import *
from r2_Gauss import *
def Normal_Fit(PeakData_and_Stats):
    PeakData=PeakData_and_Stats[0]
    GaussStats=PeakData_and_Stats[1]
    mz=GaussStats[0]
    mz_std=GaussStats[1]
    I_total=GaussStats[4]
    GaussianParameters=list(curve_fit(GaussianPeak, xdata=PeakData[:,0], ydata=PeakData[:,1],p0=[mz,mz_std,I_total])[0])
    r2=r2_Gauss(PeakData,GaussianParameters)
    NormalParameters=GaussianParameters+r2
    return NormalParameters
```

## Key operations
- Extracts initial guesses (`mz`, `mz_std`, `I_total`) from `GaussStats` (pre-fit stats from `mzPeak`).
- Calls `scipy.optimize.curve_fit` with `GaussianPeak` as the model.
- Computes coefficient of determination via [`r2_Gauss`](./r2_Gauss.md).
- Returns `[mz_fit, mz_std_fit, I_total_fit, r²]`.

## Parameters
- `PeakData_and_Stats`: tuple/list containing `PeakData` (Nx2 array of `[m/z, intensity]`) and `GaussStats` (initial parameters).

## Input
- Provided by `mzPeak` inside [`ms2_features_stats`](./ms2_features_stats.md).

## Output
- `NormalParameters`: list `[mz, mz_std, I_total, r²]`.

## Functions
- [`GaussianPeak`](./GaussianPeak.md)
- [`r2_Gauss`](./r2_Gauss.md)
- `scipy.optimize.curve_fit`

## Called by
- [`ms2_features_stats`](./ms2_features_stats.md)
- Chromatogram GA modules when refining peaks.

## Examples
```python
import numpy as np
from Functions.Normal_Fit import Normal_Fit

PeakData = np.array([
    [300.120, 1.0e5],
    [300.123, 1.5e5],
    [300.126, 1.0e5]
])
GaussStats = [300.123, 0.002, None, None, PeakData[:,1].sum()]
PeakData_and_Stats = [PeakData, GaussStats, 10021]
params = Normal_Fit(PeakData_and_Stats)
print('mz_fit:', params[0], 'r2:', params[3])
```
Plotting the fitted curve:
```python
import matplotlib.pyplot as plt
from Functions.GaussianPeak import GaussianPeak
mz_axis = np.linspace(300.118, 300.128, 200)
fit_curve = GaussianPeak(mz_axis, params[0], params[1], params[2])
plt.plot(PeakData[:,0], PeakData[:,1], 'o', label='MS1 data')
plt.plot(mz_axis, fit_curve, '-', label='Gaussian fit')
plt.legend(); plt.show()
```
