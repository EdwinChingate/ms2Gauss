---
title: GaussianPeak
kind: function
source: Functions/GaussianPeak.py
last_updated: 2025-02-14
---

## Description
`GaussianPeak` evaluates a normalized Gaussian curve across an m/z grid. It is the core model for both MS1 and MS2 peaks, providing the theoretical intensity profile used by [`Normal_Fit`](./Normal_Fit.md) and downstream chromatogram deconvolution modules. 

**Math notes**  
Given centroid \(\mu\), standard deviation \(\sigma\), and integrated intensity \(I_{\text{total}}\), the function returns
\[
I(m/z) = \frac{I_{\text{total}}}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(m/z-\mu)^2}{2\sigma^2}\right)
\]
which preserves \(\int I(m/z)\,dm/z = I_{\text{total}}\).

## Code
```python
import numpy as np
def GaussianPeak(mz_vec,mz,mz_std,I_total):
    LogVec=-((mz_vec-mz)/mz_std)**2/2
    f1_sqrt2pi=0.3989422804014327 #1/np.sqrt(np.pi*2)
    Gaussian_Int=np.exp(LogVec)*f1_sqrt2pi*I_total/mz_std
    return Gaussian_Int
```

## Key operations
- Computes the exponent term `LogVec` to avoid repeated power operations.
- Uses the precomputed factor `1/sqrt(2π)` for speed and numerical stability.
- Returns a numpy vector matching the length of `mz_vec`.

## Parameters
- `mz_vec (np.ndarray)`: Axis of m/z values where the Gaussian will be evaluated.
- `mz (float)`: Gaussian centroid (Da); corresponds to the precursor or fragment mass.
- `mz_std (float)`: Standard deviation (Da); derived from resolving power.
- `I_total (float)`: Integrated intensity ensuring area conservation.

## Input
- Called by [`Normal_Fit`](./Normal_Fit.md) with peak windows from [`mzPeak`](./mzPeak.md) or chromatogram solvers.

## Output
- Returns `Gaussian_Int`, a numpy array of modeled intensities aligned with `mz_vec`.

## Functions
- Uses `numpy` only.

## Called by
- [`Normal_Fit`](./Normal_Fit.md) when fitting MS1 peaks.
- Chromatogram simulation utilities (e.g., `GaussianChromatogram`, GA modules).

## Examples
```python
import numpy as np
import matplotlib.pyplot as plt
from Functions.GaussianPeak import GaussianPeak

mz_axis = np.linspace(300.11, 300.14, 400)
model = GaussianPeak(mz_axis, mz=300.125, mz_std=2e-3, I_total=1e6)

plt.plot(mz_axis, model)
plt.xlabel('m/z (Da)')
plt.ylabel('Intensity (a.u.)')
plt.title('Gaussian peak at 300.125 Da')
plt.show()
```
This snippet generates the theoretical profile used when estimating MS1 centroid and standard deviation.
