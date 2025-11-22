---
title: AdjacencyListFeatures
kind: function
source: Functions/AdjacencyListFeatures.py
last_updated: 2025-02-14
---

## Description
`AdjacencyListFeatures` builds RT/m/z neighborhood lists for MS2 features. Each feature’s m/z confidence interval and RT umbrella are compared against every other feature to determine potential matches. The result drives graph-based clustering in [`ms2_feat_modules`](./ms2_feat_modules.md), [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md), and [`Cluster_ms2_Features`](./Cluster_ms2_Features.md).

## Code
```python
import numpy as np
def AdjacencyListFeatures(MS2_features,mz_col=3,mz_CI_col=8,RT_col=2,minRT_col=12,maxRT_col=13,RT_tol=0,mz_Tol=0):
    N_possible_feat=len(MS2_features[:,0])
    if mz_Tol==0:
        mz_CI_Vec=MS2_features[:,mz_CI_col]
    else:
        mz_CI_Vec=np.ones(N_possible_feat)*mz_Tol
    mzVec=MS2_features[:,mz_col]
    mzMaxVec=mzVec+mz_CI_Vec
    mzMinVec=mzVec-mz_CI_Vec
    if RT_tol==0:
        RTMaxVec=MS2_features[:,maxRT_col]
        RTMinVec=MS2_features[:,minRT_col]
    else:
        RTMaxVec=MS2_features[:,RT_col]+RT_tol
        RTMinVec=MS2_features[:,RT_col]-RT_tol
    AdjacencyList=[]
    feat_ids=[]
    for feat_id in np.arange(N_possible_feat):
        min_mz=mzMinVec[feat_id]
        max_mz=mzMaxVec[feat_id]
        min_RT=RTMinVec[feat_id]
        max_RT=RTMaxVec[feat_id]
        NearFilter=(mzMaxVec>=min_mz)&(mzMinVec<=max_mz)&(RTMaxVec>=min_RT)&(RTMinVec<=max_RT)
        Neigbours=np.where(NearFilter)[0]
        AdjacencyList.append(Neigbours)
        if len(Neigbours)>0:
            feat_ids.append(feat_id)
    feat_ids=set(feat_ids)
    return [AdjacencyList,feat_ids]
```

## Key operations
- Derives m/z bounds from either the per-feature CI (`mz_CI_col`) or a fixed tolerance `mz_Tol`.
- Derives RT bounds from umbrella columns or ±`RT_tol` windows.
- Marks neighbors when intervals overlap in both dimensions.

## Parameters
- `MS2_features (np.ndarray)`: typically [`MS2_Features`](../Variables/MS2_Features.md) or [`All_FeaturesTable`](../Variables/All_FeaturesTable.md).
- `mz_col`, `mz_CI_col`, `RT_col`, `minRT_col`, `maxRT_col`: column indices.
- `RT_tol`, `mz_Tol`: override tolerances.

## Input
- Passed arrays from feature tables.

## Output
- `AdjacencyList`: list of numpy index arrays.
- `feat_ids`: set of features having at least one neighbor.

## Functions
- Uses numpy only.

## Called by
- [`ms2_feat_modules`](./ms2_feat_modules.md)
- [`Cluster_ms2_Features`](./Cluster_ms2_Features.md)
- [`ms2_SpectralSimilarityClustering`](./ms2_SpectralSimilarityClustering.md)

## Examples
```python
import numpy as np
from Functions.AdjacencyListFeatures import AdjacencyListFeatures

features = np.array([
    [0,0,245.0,300.123,0,0,0,0,1e-4,0,0,0,240,248],
    [0,0,246.0,300.124,0,0,0,0,1e-4,0,0,0,241,249]
])
AdjList, ids = AdjacencyListFeatures(features, mz_col=3, mz_CI_col=8, RT_col=2)
print(ids)
```
Plotting adjacency density:
```python
import matplotlib.pyplot as plt
neighbor_counts = [len(nei) for nei in AdjList]
plt.bar(range(len(neighbor_counts)), neighbor_counts)
plt.xlabel('Feature index')
plt.ylabel('# neighbors')
plt.show()
```
