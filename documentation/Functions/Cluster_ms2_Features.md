---
title: Cluster_ms2_Features
kind: function
source: Functions/Cluster_ms2_Features.py
last_updated: 2025-02-14
---

## Description
`Cluster_ms2_Features` takes the raw [`MS2_Features`](../Variables/MS2_Features.md) array, builds adjacency relationships via [`AdjacencyListFeatures`](./AdjacencyListFeatures.md), groups them with [`ms2_feat_modules`](./ms2_feat_modules.md), and collapses each module into a representative feature. It outputs a pandas DataFrame with averaged metadata (mz, RT, uncertainties) and aggregated umbrella statistics.

## Code
```python
import numpy as np
import pandas as pd
from ms2_feat_modules import *
from AdjacencyListFeatures import *
def Cluster_ms2_Features(MS2_features):
    AdjacencyList,feat_ids=AdjacencyListFeatures(MS2_features=MS2_features)
    Modules=ms2_feat_modules(AdjacencyList=AdjacencyList,ms2_ids=feat_ids)
    ms2_FeaturesTable=[]
    for mod in Modules:
        MS2_feature=MS2_features[mod,:].copy()
        MS2_feature=MS2_feature[(-MS2_feature[:,5]).argsort(),:]
        min_RT=np.min(MS2_feature[:,12])
        max_RT=np.max(MS2_feature[:,13])
        N_spec=np.sum(MS2_feature[:,14])
        MS2_feature[0,12]=np.max([min_RT,0])
        MS2_feature[0,13]=max_RT
        MS2_feature[0,14]=N_spec
        ms2_FeaturesTable.append(MS2_feature[0,:])
    ms2_FeaturesTable=np.array(ms2_FeaturesTable)
    ms2_FeaturesTable=ms2_FeaturesTable[ms2_FeaturesTable[:,3].argsort(),:]
    FeaturesColumns=["ms2_id",
                "ms1_id",
                "RT_(s)",
                "mz_(Da)",
                "mz_std_(Da)",
                "I_tol_1spec",
                "Gauss_r2",
                "N_points_1spec",
                "ConfidenceInterval_(Da)",
                "ConfidenceInterval_(ppm)",
                "min_mz_(Da)",
                "max_mz_(Da)",
                "min_RT_(s)",
               "max_RT_(s)",
               "N_ms2_spec",
                "spectra_id"]
    ms2_FeaturesDF=pd.DataFrame(ms2_FeaturesTable,columns=FeaturesColumns)
    return ms2_FeaturesDF
```

## Key operations
- Builds connectivity between features that share similar m/z/RT to reduce redundancy beyond single samples.
- Within each module, sorts rows by intensity (column 5) descending and takes the top row as representative.
- Updates umbrella statistics (min/max RT, total N_ms2_spec) to reflect the entire module.
- Converts numpy array to pandas DataFrame with descriptive column names for easier export.

## Parameters
- `MS2_features (np.ndarray)`: output of [`feat_ms2_Gauss`](./feat_ms2_Gauss.md).

## Input
- [`MS2_Features`](../Variables/MS2_Features.md)

## Output
- pandas DataFrame `ms2_FeaturesDF` ready for writing to Excel or aligning across samples.

## Functions
- [`AdjacencyListFeatures`](./AdjacencyListFeatures.md)
- [`ms2_feat_modules`](./ms2_feat_modules.md)

## Called by
- Commented hook inside [`feat_ms2_Gauss`](./feat_ms2_Gauss.md) and future workflows needing post-processing clusters.

## Examples
```python
import numpy as np
from Functions.Cluster_ms2_Features import Cluster_ms2_Features

MS2_features = np.array([
    [18240, 10021, 245.6, 300.1234, 1.5e-03, 8.2e05, 0.997, 28, 1.2e-04, 0.40, 299.118, 301.129, 240.1, 248.3, 3, 7021],
    [18241, 10022, 245.8, 300.1235, 1.4e-03, 7.9e05, 0.995, 26, 1.3e-04, 0.43, 299.119, 301.130, 240.5, 248.5, 2, 7022]
])
ms2_df = Cluster_ms2_Features(MS2_features)
print(ms2_df.head())
```
Plot aggregated intensities:
```python
import matplotlib.pyplot as plt
plt.bar(ms2_df['ms2_id'], ms2_df['I_tol_1spec'])
plt.xlabel('Representative ms2_id')
plt.ylabel('Intensity (a.u.)')
plt.show()
```
