---
title: AdjacencyList_from_matrix
kind: function
source: Functions/AdjacencyList_from_matrix.py
last_updated: 2025-02-14
---

## Description
Transforms a similarity matrix (e.g., cosine scores) into an adjacency list by thresholding entries above `minAdjacency`. Used to build graph representations for clustering.

## Code
```python
import numpy as np
def AdjacencyList_from_matrix(AdjacencyMatrix,N_ms2_spectra,minAdjacency=0):
    AdjacencyList=[]
    ms2_ids=[]
    for ms2_candidate_id in np.arange(N_ms2_spectra,dtype='int'):
        Neigbours=np.where(AdjacencyMatrix[ms2_candidate_id,:]>minAdjacency)[0]
        if len(Neigbours)>0:
            ms2_ids.append(ms2_candidate_id)
        AdjacencyList.append(Neigbours)
    ms2_ids=set(ms2_ids)
    return [AdjacencyList,ms2_ids]
```

## Output
- `AdjacencyList`: list of neighbor indices.
- `ms2_ids`: set of vertices with at least one neighbor.

## Called by
- [`ms2_FeaturesDifferences`](./ms2_FeaturesDifferences.md)

## Example
```python
AdjList, ids = AdjacencyList_from_matrix(CosineMat, N_ms2_spectra=len(CosineMat), minAdjacency=0.9)
```
