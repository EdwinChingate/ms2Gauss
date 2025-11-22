---
title: feat_ms2_Gauss
kind: function
source: Functions/feat_ms2_Gauss.py
last_updated: 2025-02-14
---

## Description
`feat_ms2_Gauss` iterates over every MS2 detection in [`SummMS2`](../Variables/SummMS2.md), calls [`ms2_features_stats`](./ms2_features_stats.md) to obtain MS1-refined Gaussian parameters, and aggregates the results into the [`MS2_Features`](../Variables/MS2_Features.md) array. Chromatographic umbrella metadata (`min_RT`, `max_RT`, `N_spec`, `ms2_spec_id`) are appended from `SummMS2` to preserve MS2 provenance.

## Code
```python
import numpy as np
from ms2_features_stats import *
from Cluster_ms2_Features import *
def feat_ms2_Gauss(DataSet,SummMS2,MS1IDVec,mz_std=2e-3,MS2_to_MS1_ratio=10,stdDistance=3,MaxCount=3,Points_for_regression=5,minSignals=7):
    MS2_features=[]
    N_MS2_features=len(SummMS2[:,0])
    for MS2_id in np.arange(N_MS2_features,dtype='int'):
        while True:
            try:
                min_RT=SummMS2[MS2_id,5]
                max_RT=SummMS2[MS2_id,6]
                N_spec=SummMS2[MS2_id,7]
                ms2_spec_id=int(SummMS2[MS2_id,8])
                features_stats=ms2_features_stats(DataSet=DataSet,MS2_id=MS2_id,SummMS2=SummMS2,MS1IDVec=MS1IDVec,mz_std=mz_std,MS2_to_MS1_ratio=MS2_to_MS1_ratio,stdDistance=stdDistance,MaxCount=MaxCount,Points_for_regression=Points_for_regression,minSignals=minSignals)
                if len(features_stats)>0:
                    MS2_features.append(features_stats+[min_RT]+[max_RT]+[N_spec]+[ms2_spec_id])
                break
            except:
                print('error',MS2_id)
                break
    MS2_features=np.array(MS2_features)
    MS2_features=MS2_features[MS2_features[:,3].argsort(),:]
   # ms2_FeaturesDF=Cluster_ms2_Features(MS2_features)
    return MS2_features#ms2_FeaturesDF
```

## Key operations
- Loops through every MS2 entry, ensuring umbrella metadata are captured alongside Gaussian fits.
- Wraps the call to [`ms2_features_stats`](./ms2_features_stats.md) in a `try/except` to prevent the batch run from crashing.
- Sorts the resulting array by fitted m/z (`MS2_features[:,3]`).
- Optionally supports feature clustering (currently commented out) through [`Cluster_ms2_Features`](./Cluster_ms2_Features.md).

## Parameters
- `DataSet`: iterable of MS1 spectra (see [`DataSet`](../Variables/DataSet.md)).
- `SummMS2`: MS2 summary table.
- `MS1IDVec`: MS1 scan mapping.
- `mz_std`, `stdDistance`, `MaxCount`, `Points_for_regression`, `minSignals`: forwarded to [`ms2_features_stats`](./ms2_features_stats.md).
- `MS2_to_MS1_ratio`: ratio of MS1 scans to inspect per MS2 event.

## Input
- [`DataSet`](../Variables/DataSet.md)
- [`SummMS2`](../Variables/SummMS2.md)
- [`MS1IDVec`](../Variables/MS1IDVec.md)

## Output
- [`MS2_Features`](../Variables/MS2_Features.md)

## Functions
- [`ms2_features_stats`](./ms2_features_stats.md)
- [`Cluster_ms2_Features`](./Cluster_ms2_Features.md) (optional)

## Called by
- Workflow notebooks constructing MS2-first feature tables.

## Examples
```python
import numpy as np
from Functions.feat_ms2_Gauss import feat_ms2_Gauss

DataSet = [...]
SummMS2 = np.array([
    [300.123, 245.6, 18240, 1.2e6, 0.34, 240.1, 248.3, 3, 7021],
    [450.201, 512.3, 19305, 8.5e5, 0.42, 509.7, 516.8, 2, 7150]
])
MS1IDVec = np.array([[18000, 245.2], [18005, 245.5], [18010, 245.8]])
MS2_features = feat_ms2_Gauss(DataSet, SummMS2, MS1IDVec)
```
Visualize fitted m/z vs. umbrella RT:
```python
import matplotlib.pyplot as plt
plt.scatter(MS2_features[:,3], MS2_features[:,4], c=MS2_features[:,6])
plt.xlabel('mz (Da)')
plt.ylabel('mz_std (Da)')
plt.title('Gaussian widths by feature (color = r²)')
plt.colorbar(label='Gauss r²')
plt.show()
```
