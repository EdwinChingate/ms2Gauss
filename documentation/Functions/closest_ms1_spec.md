---
title: closest_ms1_spec
kind: function
source: Functions/closest_ms1_spec.py
last_updated: 2025-02-14
---

## Description
`closest_ms1_spec` selects MS1 scan indices that immediately precede a given MS2 event. It filters [`MS1IDVec`](../Variables/MS1IDVec.md) to scans acquired before `MS2_Fullsignal_id`, computes RT differences relative to the MS2 RT, and returns the scan IDs sorted by proximity. This ensures Gaussian fits in [`ms2_features_stats`](./ms2_features_stats.md) use the most relevant chromatographic slices.

## Code
```python
import numpy as np
def closest_ms1_spec(mz,RT,MS2_Fullsignal_id,SummMS2,MS1IDVec,MS2_to_MS1_ratio=10):
    ID_filter=(MS1IDVec[:,0]<MS2_Fullsignal_id)&(MS1IDVec[:,0]>(MS2_Fullsignal_id-MS2_to_MS1_ratio)) #The MS2 is generated with the ions from the MS1, so the MS2 RT and id, would be higher
    Earlier_MS1IDVec=MS1IDVec[ID_filter,:]
    RT_DifVec=RT-Earlier_MS1IDVec[:,1]
    Min_RT_Dif=np.min(RT_DifVec)
    Closest_MS1_Loc=np.where(RT_DifVec==Min_RT_Dif)[0]
    spectrum_idVec=Earlier_MS1IDVec[RT_DifVec.argsort(),0]
    return spectrum_idVec
```

## Key operations
- Limits the search to `MS2_to_MS1_ratio` scans before the MS2 event, assuming DDA scheduling.
- Computes `RT_DifVec` and sorts ascending to prioritize MS1 scans closest in time.
- Returns only the scan IDs (first column) for downstream extraction.

## Parameters
- `mz (float)`: not used internally but retained for compatibility.
- `RT (float)`: MS2 retention time.
- `MS2_Fullsignal_id (int)`: MS2 scan index.
- `SummMS2`: not used; kept for symmetry with other functions.
- `MS1IDVec`: array of `[MS1_scan_id, RT]` pairs.
- `MS2_to_MS1_ratio (int)`: window size in scan counts.

## Input
- Provided with `MS1IDVec` from `MS_L_IDs` and metadata from [`SummMS2`](../Variables/SummMS2.md).

## Output
- `spectrum_idVec`: numpy array of MS1 scan IDs sorted by RT proximity.

## Functions
- Uses numpy only.

## Called by
- [`ms2_features_stats`](./ms2_features_stats.md)
- Chromatogram reconstruction helpers (e.g., `RetrieveChromatogram`).

## Examples
```python
import numpy as np
from Functions.closest_ms1_spec import closest_ms1_spec

MS1IDVec = np.array([[18000, 245.1], [18001, 245.3], [18002, 245.5], [18003, 245.8]])
SummMS2 = np.array([[300.12, 245.6, 18240]])
spectrum_ids = closest_ms1_spec(mz=300.12, RT=245.6, MS2_Fullsignal_id=18240,
                                 SummMS2=SummMS2, MS1IDVec=MS1IDVec, MS2_to_MS1_ratio=5)
print(spectrum_ids)
```
This returns MS1 scan IDs ordered by proximity to the MS2 RT for subsequent Gaussian fitting.
